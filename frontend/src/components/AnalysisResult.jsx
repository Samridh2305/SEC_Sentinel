import {
    AlertCircle,
    CheckCircle2,
    Plus,
    Minus,
    Pencil,
    Circle
} from "lucide-react";


const findingIcons = {
    NEW: Plus,
    REMOVED: Minus,
    MODIFIED: Pencil,
    UNCHANGED: Circle
};


function AnalysisResult({ result }) {

    if (!result) {
        return null;
    }

    const findings = result.findings ?? [];

    const summary =
        result.summary ??
        result.answer ??
        "No summary available.";


    return (
        <section className="results-section">

            <div className="results-header">

                <div>
                    <h2>Analysis Results</h2>

                    <p>
                        SEC Sentinel identified the following changes.
                    </p>
                </div>

            </div>


            {/* Summary */}

            <div className="summary-card">

                <div className="summary-icon">
                    <CheckCircle2 size={20} />
                </div>

                <div>

                    <h3>Summary</h3>

                    <p>
                        {summary}
                    </p>

                </div>

            </div>


            {/* Findings */}

            <div className="findings-container">

                <div className="findings-title">

                    <h3>Findings</h3>

                    <span>
                        {findings.length} findings
                    </span>

                </div>


                {findings.length === 0 ? (

                    <div className="no-findings">
                        No structured findings are available yet.
                    </div>

                ) : (

                    findings.map((finding, index) => {

                        const Icon =
                            findingIcons[finding.type] ||
                            AlertCircle;

                        const currentChunks =
                            finding.current_chunks ?? [];

                        const previousChunks =
                            finding.previous_chunks ?? [];


                        return (
                            <div
                                className="finding-card"
                                key={index}
                            >

                                <div className="finding-top">

                                    <div className="finding-type">

                                        <div className="finding-icon">
                                            <Icon size={17} />
                                        </div>

                                        <span
                                            className={`finding-badge ${finding.type.toLowerCase()}`}
                                        >
                                            {finding.type}
                                        </span>

                                        <span className="finding-category">
                                            {finding.category}
                                        </span>

                                    </div>

                                </div>


                                <h3>
                                    {finding.title}
                                </h3>


                                <p className="finding-description">
                                    {finding.description}
                                </p>


                                <div className="significance">

                                    <strong>
                                        Significance
                                    </strong>

                                    <p>
                                        {finding.significance}
                                    </p>

                                </div>


                                <div className="evidence">

                                    <div>

                                        <strong>
                                            Current chunks
                                        </strong>

                                        <div className="chunk-list">

                                            {currentChunks.length > 0
                                                ? currentChunks.map(
                                                    (chunk) => (
                                                        <span key={chunk}>
                                                            {chunk}
                                                        </span>
                                                    )
                                                )
                                                : "—"
                                            }

                                        </div>

                                    </div>


                                    <div>

                                        <strong>
                                            Previous chunks
                                        </strong>

                                        <div className="chunk-list">

                                            {previousChunks.length > 0
                                                ? previousChunks.map(
                                                    (chunk) => (
                                                        <span key={chunk}>
                                                            {chunk}
                                                        </span>
                                                    )
                                                )
                                                : "—"
                                            }

                                        </div>

                                    </div>

                                </div>

                            </div>
                        );
                    })
                )}

            </div>

        </section>
    );
}

export default AnalysisResult;