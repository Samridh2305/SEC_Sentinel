import { ChevronDown } from "lucide-react";

function CompanySelector({ value, onChange, companies }) {
    return (
        <div className="field">

            <label>Company</label>

            <div className="select-wrapper">

                <select
                    value={value}
                    onChange={onChange}
                    disabled={companies.length === 0}
                >

                    <option value="">
                        {companies.length === 0
                            ? "Search for a company first"
                            : "Select company"}
                    </option>

                    {companies.map((company) => (

                        <option
                            key={company.cik}
                            value={company.ticker}
                        >
                            {company.company} ({company.ticker})
                        </option>

                    ))}

                </select>

                <ChevronDown size={18} />

            </div>

        </div>
    );
}

export default CompanySelector;