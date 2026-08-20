const API_BASE_URL = "http://localhost:8000";

export async function searchCompanies(name) {

    const response = await fetch(
        `${API_BASE_URL}/companies/search?name=${encodeURIComponent(name)}`
    );


    if (!response.ok) {

        const errorText = await response.text();

        throw new Error(
            `API Error ${response.status}: ${errorText}`
        );
    }


    return response.json();
}

export async function getAllFilings(
    ticker,
    formType
) {

    const response = await fetch(
        `${API_BASE_URL}/filings/available?ticker=${encodeURIComponent(ticker)}&form_type=${encodeURIComponent(formType)}`
    );


    if (!response.ok) {

        const errorText = await response.text();

        throw new Error(
            `API Error ${response.status}: ${errorText}`
        );
    }


    return response.json();
}

export async function askSentinel(request) {

    const response = await fetch(
        `${API_BASE_URL}/ask`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(request)
        }
    );


    if (!response.ok) {

        const errorText = await response.text();

        throw new Error(
            `API Error ${response.status}: ${errorText}`
        );
    }


    return response.json();
}