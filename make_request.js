const fs = require("fs");
const path = "am_comm.txt";

function writeRequest(request) {
    return new Promise((resolve, reject) => {
        fs.writeFile(path, request + "\n", (err) => {  // Overwrite file with request
            if (err) {
                reject("Error writing request: " + err);
            } else {
                console.log("Request sent:", request);
                resolve();
            }
        });
    });
}

function waitForResponse() {
    return new Promise((resolve, reject) => {
        let checkInterval = setInterval(() => {
            fs.readFile(path, "utf8", (err, data) => {
                if (err) {
                    clearInterval(checkInterval);
                    reject("Error reading response: " + err);
                    return;
                }

                const response = data.trim();

                // Ensure we have a full response (not just part of it)
                if (response && !response.includes(",")) { // If it's a response (not a new request)
                    // Wait a short delay to ensure entire response is written
                    setTimeout(() => {
                        fs.readFile(path, "utf8", (finalErr, finalData) => {
                            if (finalErr) {
                                clearInterval(checkInterval);
                                reject("Error reading final response: " + finalErr);
                                return;
                            }

                            const finalResponse = finalData.trim();
                            clearInterval(checkInterval);

                            // Clear the response file AFTER ensuring the full response is read
                            fs.writeFile(path, "", (writeErr) => {
                                if (writeErr) {
                                    console.error("Error clearing response:", writeErr);
                                }
                                resolve(finalResponse);
                            });
                        });
                    }, 100); // Small delay to ensure full response is captured
                }
            });
        }, 100); // Check every 100ms
    });
}

async function makeRequest() {
    const request = "1, user6, pass10"; // Example: Create an account
    await writeRequest(request);
    
    console.log("Waiting for response...");
    const response = await waitForResponse();
    
    console.log("Received Response:", response);
}

// Run the request process
makeRequest();
