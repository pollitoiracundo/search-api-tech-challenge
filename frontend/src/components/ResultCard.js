import React from 'react';

const ResultCard = ({ result }) => {
    const { number, basic, addresses, taxonomies, normalizedScore } = result;
    const primaryAddress = addresses.find(addr => addr.address_purpose === 'LOCATION') || addresses[0];
    const primaryTaxonomy = taxonomies.find(tax => tax.primary) || taxonomies[0];

    return (
        <div className="result-card">
            <h2>{basic.organization_name} {basic.name_prefix} {basic.first_name} {basic.middle_name} {basic.last_name} {basic.credential}</h2>
            <p>NPI: {number}</p>
            <p>Address: {primaryAddress.address_1}, {primaryAddress.city}, {primaryAddress.state}, {primaryAddress.postal_code}</p>
            <p>Phone: {primaryAddress.telephone_number}</p>
            <p>Taxonomy: {primaryTaxonomy.desc}</p>
            <p className="score">Score: {normalizedScore.toFixed(2)}</p>
        </div>
    );
};

export default ResultCard;