import { useState } from "react";
import { searchCompanies } from "../services/api";

function CompanySearch({ onSelect }) {

    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = async () => {

        if (!query.trim()) {
            setResults([]);
            return;
        }

        setLoading(true);
        setError(null);

        try {

            const data = await searchCompanies(query);

            setResults(data);

        } catch (error) {

            console.error(
                "Company search failed:",
                error
            );

            setError(
                error.message ||
                "Company search failed."
            );

            setResults([]);

        } finally {

            setLoading(false);
        }
    };

    const handleQueryChange = (event) => {

        setQuery(event.target.value);

        // Hide old results when user starts a new search
        setResults([]);

        setError(null);
    };

    const handleCompanySelect = (company) => {

        // Replace company name with ticker
        setQuery(company.ticker);

        // Hide search results
        setResults([]);

        // Tell Dashboard which company was selected
        onSelect(company);
    };

    return (
        <div className="company-search">

            <label>Company</label>

            <div className="search-row">

                <input
                    type="text"
                    value={query}
                    placeholder="Search company..."
                    onChange={handleQueryChange}
                    onKeyDown={(event) => {
                        if (event.key === "Enter") {
                            handleSearch();
                        }
                    }}
                />

                <button
                    type="button"
                    onClick={handleSearch}
                    disabled={loading}
                >
                    {loading
                        ? "Searching..."
                        : "Search"}
                </button>

            </div>

            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            {results.length > 0 && (
                <div className="company-results">

                    {results.map((company) => (

                        <button
                            type="button"
                            key={`${company.cik}-${company.ticker}`}
                            className="company-result"
                            onClick={() =>
                                handleCompanySelect(company)
                            }
                        >

                            <strong>
                                {company.company}
                            </strong>

                            <span>
                                {company.ticker}
                            </span>

                        </button>

                    ))}

                </div>
            )}

        </div>
    );
}

export default CompanySearch;