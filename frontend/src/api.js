import axios from 'axios';

const API_URL = 'https://tf2bfbbm83.execute-api.us-west-2.amazonaws.com/dev/search/doctors';
//const API_URL = 'http://localhost:8000/search/doctors';


export const fetchHealthProfessionals = async (query) => {
    try {
        const headers = {
            'x-api-key': 'K3lS7TYaPI7N6PdYHDSnr5pUWH119tKr5d6NlIc7'
        }
        const response = await axios.post(API_URL, {
            search: query
        }, {headers: headers});
        console.log("original_input: " + response.data.original_input)
        console.log("real_query: " + response.data.real_query)
        return response.data.res.results;
    } catch (error) {
        console.error('Error fetching data:', error);
        return [];
    }
};