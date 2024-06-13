from openai import OpenAI
import json
import logging
from npi import get_npi_query

client = OpenAI()
logger = logging.getLogger(__name__)


SYSTEM_NPI_QUERY = """
You must be able to analyze noisy JSON array inputs to create the best query parameters for calling the NPI Registry Public Search looking for individuals.
Validate and correct the content of fields such as valid cities, common names, and others. Fix and approximate fields, 
using wildcards when necessary with names cities, etc, and combine fields from different items in the noisy array.
Include all the posible fields.
The NPI Registry is a free directory of all active National Provider Identifier (NPI) records. 
If you receive a JSON array as input, call the get_npi_query and return the result."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_npi_query",
            "description": "Get the best query parameters according to the input for looking into the NPI service for individuals.",
            "parameters": {
                "type": "object",
                "properties": {
                    "version": {
                        "type": "string",
                        "description": "Always use 2.1 as version. Identifies the version of the API to use ('2.1')",
                    },
                    "number": {
                        "type": "integer",
                        "description": "The NPI Number is the unique 10-digit National Provider Identifier assigned to the provider. Exactly 10 digits.",
                    },
                    "enumeration_type": {
                        "type": "string", 
                        "enum": ["NPI-1", "NPI-2"],
                        "description":"The Read API can be refined to retrieve only Individual Providers or Organizational Providers. When it is not specified, both Type 1 and Type 2 NPIs will be returned. When using the Enumeration Type, it cannot be the only criteria entered. Additional criteria must also be entered as well. Valid values are: NPI-1: Individual Providers (Type 1) NPIs, NPI-2: Organizational Providers (Type 2) NPIs",
                    },
                    "taxonomy_description": {
                        "type": "string",
                        "description": "Search for providers by their taxonomy by entering the taxonomy description.",
                    },
                    "name_purpose": {
                        "type": "string",
                        "description": "Refers to whether the name information entered pertains to an Authorized Official's name or a Provider's name. When not specified, the results will search against a provider's first and last name. AO will only search against Authorized Official name. While PROVIDER will only search against Provider name. Valid values are: AO, Provider.",
                        "enum": ["AO", "Provider"],
                    },
                    "first_name": {
                        "type": "string",
                        "description": "This field only applies to Individual Providers. Trailing wildcard entries are permitted requiring at least two characters to be entered (e.g. 'jo*' ). This field allows the following special characters: ampersand, apostrophe, colon, comma, forward slash, hyphen, left and right parentheses, period, pound sign, quotation mark, and semi-colon.",
                    },
                    "use_first_name_alias": {
                        "type": "string",
                        "description": "This field applies to Authorized Officials and Individual Providers when not doing a wildcard search. When set to 'True', the search results will include Providers with similar First Names. E.g., first_name=Robert, will also return Authorized Officials and Providers with the first name of Rob, Bob, Robbie, Bobby, etc. Valid Values are: True, False. Default Value is True",
                    },
                    "last_name": {
                        "type": "string",
                        "description": "This field only applies to Individual Providers. Trailing wildcard entries are permitted requiring at least two characters to be entered. This field allows the following special characters: ampersand, apostrophe, colon, comma, forward slash, hyphen, left and right parentheses, period, pound sign, quotation mark, and semi-colon.",
                    },
                    "organization_name": {
                        "type": "string",
                        "description": "This field only applies to Organizational Providers. Trailing wildcard entries are permitted requiring at least two characters to be entered. This field allows the following special characters: ampersand, apostrophe, 'at' sign, colon, comma, forward slash, hyphen, left and right parentheses, period, pound sign, quotation mark, and semi-colon. All types of Organization Names (LBN, DBA, Former LBN, Other Name) associated with an NPI are examined for matching contents, therefore, the results might contain an organization name different from the one entered in the Organization Name criterion.",
                    },                    
                    "address_purpose": {
                        "type": "string",
                        "description": "Refers to whether the address information entered pertains to the provider's Mailing Address or the provider's Practice Location Address. When not specified, the results will contain the providers where either the Mailing Address or any of Practice Location Addresses match the entered address information. PRIMARY will only search against Primary Location Address. While Secondary will only search against Secondary Location Addresses. Valid values are: LOCATION, MAILING, PRIMARY, SECONDARY",
                    },                    
                    "city": {
                        "type": "string",
                        "description": "The City associated with the provider's address identified in Address Purpose. To search for a Military Address enter either APO or FPO into the City field. This field allows the following special characters: ampersand, apostrophe, colon, comma, forward slash, hyphen, left and right parentheses, period, pound sign, quotation mark, and semi-colon.",
                    },                    
                    "state": {
                        "type": "string",
                        "description": "The State abbreviation associated with the provider's address identified in Address Purpose. This field cannot be used as the only input criterion. If this field is used, at least one other field, besides the Enumeration Type and Country, must be populated. Example: AL",
                    },                    
                    "postal_code": {
                        "type": "string",
                        "description": "The Postal Code associated with the provider's address identified in Address Purpose. If you enter a 5 digit postal code, it will match any appropriate 9 digit (zip+4) codes in the data. Trailing wildcard entries are permitted requiring at least two characters to be entered (e.g., '21*').",
                    },                     
                    "country_code": {
                        "type": "string",
                        "description": "The Country associated with the provider's address identified in Address Purpose. This field can be used as the only input criterion as long as the value selected is not US (United States).",
                    },                    
                },
                "required": [],
            },
        },
    }
]


def create_npi_query(data: str):
    # Step 1: send the conversation and available functions to the model
    messages = [{"role": "system", "content": SYSTEM_NPI_QUERY}]
    messages.append({"role": "user", "content": data})
    #logger.info(messages)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",  # auto is default, but we'll be explicit
        temperature=0.0,
        top_p=0,
        frequency_penalty=2,
        presence_penalty=2
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_npi_query": get_npi_query,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            return function_to_call(function_args)

def get_embeddings_item(text):
    return client.embeddings.create(input = [text], model="text-embedding-3-small").data[0].embedding
