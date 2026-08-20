import { ChevronDown } from "lucide-react";

function FilingSelector({
    label,
    value,
    onChange,
    filings
}) {
    return (
        <div className="field">
            <label>{label}</label>

            <div className="select-wrapper">
                <select value={value} onChange={onChange}>

                    {filings.map((filing) => (
                        <option
                            key={filing.id}
                            value={filing.id}
                        >
                            {filing.label}
                        </option>
                    ))}

                </select>

                <ChevronDown size={18} />
            </div>
        </div>
    );
}

export default FilingSelector;