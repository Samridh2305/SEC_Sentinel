import { ChevronDown, Download, LoaderCircle } from "lucide-react";

function FilingSelector({
    label,
    value,
    onChange,
    filings,
    loading,
    downloadingFilings,
    onDownload
}) {

    const selectedFiling = filings.find(
        filing => filing.filing_date === value
    );

    const isDownloading =
        selectedFiling &&
        downloadingFilings.has(
            selectedFiling.filing_date
        );

    return (
        <div className="field">

            <label>{label}</label>

            <div className="select-wrapper">

                <select
                    value={value}
                    onChange={onChange}
                    disabled={loading || isDownloading}
                >

                    {loading ? (

                        <option value="">
                            Loading filings...
                        </option>

                    ) : filings.length === 0 ? (

                        <option value="">
                            No filings available
                        </option>

                    ) : (

                        filings.map((filing) => (

                            <option
                                key={filing.filing_date}
                                value={filing.filing_date}
                            >
                                {filing.filing_date}
                                {filing.in_db
                                    ? " ✓"
                                    : " — Not downloaded"}
                            </option>

                        ))

                    )}

                </select>

                <ChevronDown size={18} />

            </div>


            {/* Download selected filing */}

            {selectedFiling && !selectedFiling.in_db && (

                <button
                    type="button"
                    className="download-button"
                    onClick={() =>
                        onDownload(selectedFiling)
                    }
                    disabled={isDownloading}
                >

                    {isDownloading ? (
                        <>
                            <LoaderCircle
                                size={16}
                                className="spin"
                            />
                            Downloading...
                        </>
                    ) : (
                        <>
                            <Download size={16} />
                            Download Filing
                        </>
                    )}

                </button>

            )}

        </div>
    );
}

export default FilingSelector;