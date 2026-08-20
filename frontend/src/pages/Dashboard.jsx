import { useState } from "react";

import Sidebar from "../components/Sidebar";
import CompanySearch from "../components/CompanySearch";
import FilingSelector from "../components/FilingSelector";
import QuestionInput from "../components/QuestionInput";
import AnalysisResult from "../components/AnalysisResult";

function Dashboard() {

    const [selectedCompany, setSelectedCompany] = useState(null);

    const [formType, setFormType] = useState("10-K");

    const [filings, setFilings] = useState([]);

    const [currentFiling, setCurrentFiling] = useState("");
    const [previousFiling, setPreviousFiling] = useState("");

    const [question, setQuestion] = useState(
        "What changed in cybersecurity and supply-chain risks?"
    );

    const [result, setResult] = useState(null);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState(null);


    const handleCompanySelect = (company) => {

        console.log("Selected company:", company);

        setSelectedCompany(company);

        setFilings([]);

        setCurrentFiling("");
        setPreviousFiling("");

        setResult(null);

        setError(null);
    };


    const handleAnalyze = async () => {

        if (!selectedCompany) {

            setError("Please select a company.");

            return;
        }

        if (!currentFiling) {

            setError("Please select a current filing.");

            return;
        }

        if (!previousFiling) {

            setError("Please select a previous filing.");

            return;
        }

        if (!question.trim()) {

            setError("Please enter a question.");

            return;
        }

        setLoading(true);
        setError(null);

        try {

            // We will connect /ask here next.

            console.log("Analysis request:", {
                ticker: selectedCompany.ticker,
                form_type: formType,
                filing_date: currentFiling,
                comparison_filing_date: previousFiling,
                query: question,
                section: "Risk Factors"
            });

        } catch (error) {

            console.error("Analysis failed:", error);

            setError(
                error.message ||
                "Something went wrong while analyzing the filing."
            );

        } finally {

            setLoading(false);
        }
    };


    return (

        <div className="app">

            <Sidebar />

            <main className="main-content">

                <div className="page-header">

                    <div>

                        <h1>
                            SEC Filing Intelligence
                        </h1>

                        <p>
                            Analyze changes across SEC filings
                        </p>

                    </div>

                </div>


                <div className="analysis-container">


                    {/* Company Search */}

                    <CompanySearch
                        onSelect={handleCompanySelect}
                    />


                    {/* Selected Company */}

                    {selectedCompany && (

                        <div className="selected-company">

                            <strong>
                                {selectedCompany.company}
                            </strong>

                            <span>
                                {selectedCompany.ticker}
                            </span>

                        </div>

                    )}


                    {/* Form Type */}

                    {selectedCompany && (

                        <div className="field">

                            <label>
                                Filing Type
                            </label>

                            <div className="select-wrapper">

                                <select
                                    value={formType}
                                    onChange={(event) =>
                                        setFormType(
                                            event.target.value
                                        )
                                    }
                                >

                                    <option value="10-K">
                                        10-K
                                    </option>

                                    <option value="10-Q">
                                        10-Q
                                    </option>

                                    <option value="8-K">
                                        8-K
                                    </option>

                                </select>

                            </div>

                        </div>

                    )}


                    {/* Filings */}

                    {selectedCompany && (

                        <div className="filing-row">

                            <FilingSelector
                                label="Current Filing"
                                value={currentFiling}
                                onChange={(event) =>
                                    setCurrentFiling(
                                        event.target.value
                                    )
                                }
                                filings={filings}
                            />


                            <FilingSelector
                                label="Previous Filing"
                                value={previousFiling}
                                onChange={(event) =>
                                    setPreviousFiling(
                                        event.target.value
                                    )
                                }
                                filings={filings}
                            />

                        </div>

                    )}


                    {/* Section */}

                    {selectedCompany && (

                        <div className="field">

                            <label>
                                Section
                            </label>

                            <div className="select-wrapper">

                                <select
                                    defaultValue="Risk Factors"
                                >

                                    <option value="Risk Factors">
                                        Risk Factors
                                    </option>

                                    <option value="Business">
                                        Business
                                    </option>

                                    <option value="MD&A">
                                        MD&A
                                    </option>

                                    <option value="Financial Statements">
                                        Financial Statements
                                    </option>

                                </select>

                            </div>

                        </div>

                    )}


                    {/* Question */}

                    {selectedCompany && (

                        <QuestionInput
                            value={question}
                            onChange={(event) =>
                                setQuestion(
                                    event.target.value
                                )
                            }
                            onAnalyze={handleAnalyze}
                            loading={loading}
                        />

                    )}


                    {/* Error */}

                    {error && (

                        <div className="error-message">

                            {error}

                        </div>

                    )}


                    {/* Results */}

                    <AnalysisResult
                        result={result}
                    />

                </div>

            </main>

        </div>
    );
}

export default Dashboard;