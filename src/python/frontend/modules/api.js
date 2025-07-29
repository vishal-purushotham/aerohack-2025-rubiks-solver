// src/python/frontend/modules/api.js

export const url = "http://127.0.0.1:5000";

export async function postMove(move) {
    try {
        await fetch(url + "/move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ move: move }),
        });
    } catch (error) {
        console.error("Error sending move to backend:", error);
    }
}

export async function getSolution() {
    try {
        const response = await fetch(url + "/solve");
        if (!response.ok) throw new Error("Failed to fetch solution.");
        return await response.json();
    } catch (error) {
        console.error("Error fetching solution:", error);
        return null;
    }
}

export async function getCubeData() {
    try {
        const response = await fetch(url + "/get_cube_data");
        if (!response.ok) throw new Error("Failed to fetch cube data.");
        return await response.json();
    } catch (error) {
        console.error("Error fetching cube data:", error);
        return { state: "", solution: "Error fetching data" };
    }
}

export function resetBackendState() {
    fetch(url + '/reset-cube', { method: 'POST' })
    .catch(error => console.error("Error resetting cube:", error));
}
