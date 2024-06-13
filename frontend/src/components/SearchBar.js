import React, { useState } from 'react';

const SearchBar = ({ onSearch, loading }) => {
    const [query, setQuery] = useState('');

    const handleSearch = () => {
        onSearch(query);
    };

    return (
        <div className="search-bar">
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for profesionals and clinics"
                disabled={loading}
            />
            <button onClick={handleSearch} disabled={loading}>
                {loading ? 'Searching...' : 'Search'} 
            </button>
        </div>
    );
};

export default SearchBar;