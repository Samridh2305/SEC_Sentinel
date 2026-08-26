import { useEffect, useState } from "react";

import CompanySearch from "../components/CompanySearch";
import FilingSelector from "../components/FilingSelector";
import QuestionInput from "../components/QuestionInput";
import AnalysisResult from "../components/AnalysisResult";

import {
    getSecFilings,
    getAllFilings,
    askSentinel,
    downloadFiling,
    getIngestionJob
} from "../services/api";


function Dashboard() {

    // -------------------------
    // State
    // -------------------------

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

    const [loadingFilings, setLoadingFilings] = useState(false);

    const [downloadingFilings, setDownloadingFilings] = useState(
        new Set()
    );

    const [error, setError] = useState(null);


    // -------------------------
    // Load filings
    // -------------------------

    useEffect(() => {

        if (!selectedCompany) {
            return;
        }

        const loadFilings = async () => {

            setLoadingFilings(true);
            setError(null);

            try {

                // --------------------------------
                // 1. Get filings available from SEC
                // --------------------------------

                const secFilings = await getSecFilings(
                    selectedCompany.ticker,
                    formType
                );


                // --------------------------------
                // 2. Get filings already in our DB
                // --------------------------------

                const localData = await getAllFilings(
                    selectedCompany.ticker,
                    formType
                );


                console.log(
                    "SEC filings:",
                    secFilings
                );

                console.log(
                    "Local filings:",
                    localData
                );


                // --------------------------------
                // 3. Get dates already in our DB
                // --------------------------------

                const localDates = new Set(
                    localData.filings.map(
                        filing => filing.filing_date
                    )
                );


                // --------------------------------
                // 4. Merge SEC + local information
                // --------------------------------

                const mergedFilings = secFilings.map(
                    filing => ({
                        ...filing,

                        in_db: localDates.has(
                            filing.filing_date
                        )
                    })
                );


                console.log(
                    "Merged filings:",
                    mergedFilings
                );


                // --------------------------------
                // 5. Sort and store filings
                // --------------------------------

                const sortedFilings = [...mergedFilings].sort(
                    (a, b) =>
                        new Date(b.filing_date) -
                        new Date(a.filing_date)
                );

                setFilings(sortedFilings);

                // Automatically select newest
                setCurrentFiling(
                    sortedFilings[0]?.filing_date ?? ""
                );

                // Automatically select second-newest
                setPreviousFiling(
                    sortedFilings[1]?.filing_date ?? ""
                );

            } catch (error) {

                console.error(
                    "Failed to load filings:",
                    error
                );

                setError(
                    error.message ||
                    "Failed to load filings."
                );

            } finally {

                setLoadingFilings(false);

            }
        };


        loadFilings();

    }, [selectedCompany, formType]);


    // -------------------------
    // Company selected
    // -------------------------

    const handleCompanySelect = (company) => {

        console.log(
            "Selected company:",
            company
        );

        setSelectedCompany(company);

        setFilings([]);

        setCurrentFiling("");
        setPreviousFiling("");

        setResult(null);

        setError(null);
    };


    // -------------------------
    // Filing selection
    // -------------------------

    const handleCurrentFilingChange = (event) => {

        const value = event.target.value;

        if (value === previousFiling) {

            setError(
                "Current and Previous filings must be different."
            );

            return;
        }

        setError(null);
        setCurrentFiling(value);
    };


    const handlePreviousFilingChange = (event) => {

        const value = event.target.value;

        if (value === currentFiling) {

            setError(
                "Current and Previous filings must be different."
            );

            return;
        }

        setError(null);
        setPreviousFiling(value);
    };


    // -------------------------
    // Analyze
    // -------------------------

    const handleAnalyze = async () => {

        if (!selectedCompany) {

            setError(
                "Please select a company."
            );

            return;
        }


        if (!currentFiling) {

            setError(
                "Please select a current filing."
            );

            return;
        }


        if (!previousFiling) {

            setError(
                "Please select a previous filing."
            );

            return;
        }


        if (currentFiling === previousFiling) {

            setError(
                "Current and Previous filings must be different."
            );

            return;
        }


        const current = filings.find(
            filing =>
                filing.filing_date === currentFiling
        );

        const previous = filings.find(
            filing =>
                filing.filing_date === previousFiling
        );


        if (!current?.in_db) {

            setError(
                "The current filing has not been downloaded yet."
            );

            return;
        }


        if (!previous?.in_db) {

            setError(
                "The previous filing has not been downloaded yet."
            );

            return;
        }


        if (!question.trim()) {

            setError(
                "Please enter a question."
            );

            return;
        }


        setLoading(true);
        setError(null);


        try {

            const response = await askSentinel({

                ticker:
                    selectedCompany.ticker,

                form_type:
                    formType,

                filing_date:
                    currentFiling,

                comparison_filing_date:
                    previousFiling,

                query:
                    question

            });


            console.log(
                "Analysis response:",
                response
            );


            setResult(response);

        } catch (error) {

            console.error(
                "Analysis failed:",
                error
            );

            setError(
                error.message ||
                "Something went wrong while analyzing the filing."
            );

            setResult(null);

        } finally {

            setLoading(false);

        }
    };


    // -------------------------
    // Poll ingestion job
    // -------------------------

    const pollIngestionJob = async (jobId) => {

        while (true) {

            const job = await getIngestionJob(jobId);

            console.log(
                "Ingestion job status:",
                job
            );


            if (job.status === "COMPLETED") {

                return job;

            }


            if (job.status === "FAILED") {

                throw new Error(
                    job.error_message ||
                    "Filing ingestion failed."
                );

            }


            await new Promise(
                resolve =>
                    setTimeout(resolve, 1500)
            );
        }
    };


    // -------------------------
    // Download filing
    // -------------------------

    const handleDownload = async (filing) => {

        if (!selectedCompany) {
            return;
        }


        const filingDate = filing.filing_date;

        setError(null);


        // Add this filing to downloading set
        setDownloadingFilings(prev => {

            const next = new Set(prev);

            next.add(filingDate);

            return next;

        });


        try {

            // --------------------------------
            // Start ingestion job
            // --------------------------------

            const job = await downloadFiling(
                selectedCompany.ticker,
                formType,
                filingDate
            );


            console.log(
                "Started ingestion:",
                job
            );


            // --------------------------------
            // Wait for ingestion to finish
            // --------------------------------

            const completedJob =
                await pollIngestionJob(
                    job.job_id
                );


            console.log(
                "Ingestion completed:",
                completedJob
            );


            // --------------------------------
            // Refresh filings
            // --------------------------------

            const secFilings =
                await getSecFilings(
                    selectedCompany.ticker,
                    formType
                );


            const localData =
                await getAllFilings(
                    selectedCompany.ticker,
                    formType
                );


            const localDates = new Set(
                localData.filings.map(
                    filing =>
                        filing.filing_date
                )
            );


            const mergedFilings =
                secFilings.map(
                    filing => ({
                        ...filing,

                        in_db:
                            localDates.has(
                                filing.filing_date
                            )
                    })
                );


            const sortedFilings =
                [...mergedFilings].sort(
                    (a, b) =>
                        new Date(b.filing_date) -
                        new Date(a.filing_date)
                );


            setFilings(sortedFilings);

        } catch (error) {

            console.error(
                "Filing download failed:",
                error
            );

            setError(
                error.message ||
                "Failed to download filing."
            );

        } finally {

            // Remove only THIS filing
            setDownloadingFilings(prev => {

                const next = new Set(prev);

                next.delete(filingDate);

                return next;

            });
        }
    };


    // -------------------------
    // Render
    // -------------------------

    return (

        <div className="app">

            <main className="main-content">

                {/* Page Header */}

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


                    {/* Filing Type */}

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
                                onChange={
                                    handleCurrentFilingChange
                                }
                                filings={filings}
                                loading={loadingFilings}
                                downloadingFilings={
                                    downloadingFilings
                                }
                                onDownload={
                                    handleDownload
                                }
                            />


                            <FilingSelector
                                label="Previous Filing"
                                value={previousFiling}
                                onChange={
                                    handlePreviousFilingChange
                                }
                                filings={filings}
                                loading={loadingFilings}
                                downloadingFilings={
                                    downloadingFilings
                                }
                                onDownload={
                                    handleDownload
                                }
                            />

                        </div>

                    )}


                    {/* No filings */}

                    {selectedCompany &&
                        !loadingFilings &&
                        filings.length === 0 && (

                            <div className="error-message">

                                No {formType} filings are available
                                for{" "}
                                {selectedCompany.ticker}.

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
                            loading={
                                loading ||
                                loadingFilings
                            }
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