import React, { useState } from "react";
import SearchBar from "./components/SearchBar";
import ResultCard from "./components/ResultCard";
import { fetchHealthProfessionals } from "./api";
import "./App.css";

const normalizeScore = (score, minScore, maxScore) => {
  return ((score - minScore) / (maxScore - minScore)) * 9 + 1;
};

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [noResults, setNoResults] = useState(false);

  const handleSearch = async (query) => {
    setLoading(true);
    setNoResults(false);

    const fetchedResults = await fetchHealthProfessionals(query);

    if (fetchedResults.length === 0) {
      setResults([]);
      setNoResults(true);
      setLoading(false);
      return;
    }

    const minScore = Math.min(...fetchedResults.map((result) => result.score));
    const maxScore = Math.max(...fetchedResults.map((result) => result.score));

    const normalizedResults = fetchedResults.map((result) => ({
      ...result,
      normalizedScore: normalizeScore(result.score, minScore, maxScore),
    }));

    normalizedResults.sort((a, b) => b.normalizedScore - a.normalizedScore);

    setResults(normalizedResults);
    setLoading(false);
  };
  return (
    <div className="App">
      <SearchBar onSearch={handleSearch} loading={loading} />
      <div className="results">
        {noResults ? (
          <p>No results.</p>
        ) : (
          results.map((result) => (
            <ResultCard key={result.number} result={result} />
          ))
        )}
      </div>
    </div>
  );
}

export default App;
