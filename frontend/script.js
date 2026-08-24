const API_URL = "https://ai-resume-analyzer-75gi.onrender.com";

let resumeSkills = [];
let resumeText = "";
window.resumeScore = 0;


// =========================================
// HELPER FUNCTIONS
// =========================================

function safeArray(value) {
    return Array.isArray(value) ? value : [];
}


function renderList(items, emptyText = "No information available.") {

    const list = safeArray(items);

    if (!list.length) {
        return `<li>${emptyText}</li>`;
    }

    return list
        .map(item => `<li>${item}</li>`)
        .join("");
}


function renderParagraph(value, emptyText = "No information available.") {

    if (!value) {
        return `<p>${emptyText}</p>`;
    }

    return `<p>${value}</p>`;
}


// =========================================
// RESUME ANALYZER
// =========================================

async function analyzeResume() {

    const fileInput =
        document.getElementById("resumeFile");

    const message =
        document.getElementById("message");


    if (!fileInput.files.length) {

        message.innerHTML =
            "❌ Please select a resume first.";

        return;
    }


    const file =
        fileInput.files[0];


    const formData =
        new FormData();

    formData.append(
        "resume",
        file
    );


    message.innerHTML = `
        <div class="loading">
            ⏳ AI is analyzing your resume...
            <br>
            <small>This may take a few seconds.</small>
        </div>
    `;


    try {

        const response =
            await fetch(
                `${API_URL}/analyze`,
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            message.innerHTML =
                "❌ " +
                (
                    data.error ||
                    "Something went wrong."
                );

            return;
        }


        // =====================================
        // SAVE DATA
        // =====================================

        resumeSkills =
            data.skills || [];


        resumeText =
            data.text || "";


        window.resumeScore =
            data.score
                ? data.score.total
                : 0;


        const contact =
            data.contact || {};


        const score =
            data.score || {

                total: 0,
                contact: 0,
                education: 0,
                skills: 0,
                experience: 0,
                projects: 0,
                objective: 0
            };


        const ai =
            data.ai_analysis || {};


        // =====================================
        // AI DATA
        // =====================================

        const summary =
            ai.summary ||
            "AI summary is not available.";


        const strengths =
            safeArray(ai.strengths);


        const weaknesses =
            safeArray(ai.weaknesses);


        const missingSkills =
            safeArray(ai.missing_skills);


        const improvementsAI =
            safeArray(ai.improvements);


        const projects =
            safeArray(ai.recommended_projects);


        const interviewQuestions =
            safeArray(ai.interview_questions);


        const careerSuggestions =
            safeArray(ai.career_suggestions);


        const atsAnalysis =
            ai.ats_analysis ||
            "ATS analysis is not available.";


        // =====================================
        // DISPLAY RESULT
        // =====================================

        message.innerHTML = `

            <div class="result-container">

                <!-- BASIC INFORMATION -->

                <h3>✅ Resume Analyzed Successfully</h3>

                <hr>

                <h3>👤 Candidate Information</h3>

                <p>
                    <strong>Name:</strong>
                    ${contact.name || "Not detected"}
                </p>

                <p>
                    <strong>Email:</strong>
                    ${contact.email || "Not detected"}
                </p>

                <p>
                    <strong>Phone:</strong>
                    ${contact.phone || "Not detected"}
                </p>


                <!-- SKILLS -->

                <h3>🛠️ Detected Skills</h3>

                <p>
                    ${
                        resumeSkills.length
                            ? resumeSkills.join(", ")
                            : "No skills detected."
                    }
                </p>


                <!-- RESUME SCORE -->

                <hr>

                <h3>🎯 Resume Score</h3>

                <h1>
                    ${score.total}/100
                </h1>


                <div class="score-details">

                    <p>
                        Contact Information:
                        <strong>
                            ${score.contact}/10
                        </strong>
                    </p>

                    <p>
                        Education:
                        <strong>
                            ${score.education}/20
                        </strong>
                    </p>

                    <p>
                        Skills:
                        <strong>
                            ${score.skills}/20
                        </strong>
                    </p>

                    <p>
                        Experience:
                        <strong>
                            ${score.experience}/20
                        </strong>
                    </p>

                    <p>
                        Projects:
                        <strong>
                            ${score.projects}/20
                        </strong>
                    </p>

                    <p>
                        Objective:
                        <strong>
                            ${score.objective}/10
                        </strong>
                    </p>

                </div>


                <!-- ================================= -->
                <!-- REAL AI ANALYSIS -->
                <!-- ================================= -->

                <hr>

                <h2>🤖 AI Resume Analysis</h2>


                <!-- SUMMARY -->

                <h3>🧠 AI Summary</h3>

                ${renderParagraph(summary)}


                <!-- STRENGTHS -->

                <h3>💪 Resume Strengths</h3>

                <ul>

                    ${renderList(
                        strengths,
                        "No specific strengths detected."
                    )}

                </ul>


                <!-- WEAKNESSES -->

                <h3>⚠️ Resume Weaknesses</h3>

                <ul>

                    ${renderList(
                        weaknesses,
                        "No major weaknesses detected."
                    )}

                </ul>


                <!-- MISSING SKILLS -->

                <h3>📚 Missing Skills</h3>

                <ul>

                    ${renderList(
                        missingSkills,
                        "No major missing skills identified."
                    )}

                </ul>


                <!-- ATS -->

                <h3>📋 ATS Analysis</h3>

                ${renderParagraph(
                    atsAnalysis
                )}


                <!-- AI IMPROVEMENTS -->

                <h3>💡 Personalized AI Improvements</h3>

                <ul>

                    ${
                        improvementsAI.length
                            ? renderList(
                                improvementsAI
                            )
                            : renderList(
                                data.improvements || [],
                                "No improvements available."
                            )
                    }

                </ul>


                <!-- PROJECTS -->

                <h3>🚀 Recommended Projects</h3>

                <ul>

                    ${renderList(
                        projects,
                        "No project recommendations available."
                    )}

                </ul>


                <!-- INTERVIEW QUESTIONS -->

                <h3>🎤 Personalized Interview Questions</h3>

                <ol>

                    ${
                        interviewQuestions.length
                            ? interviewQuestions
                                .map(
                                    question =>
                                        `<li>${question}</li>`
                                )
                                .join("")
                            : "<li>No interview questions generated.</li>"
                    }

                </ol>


                <!-- CAREER -->

                <h3>🎯 Career Suggestions</h3>

                <ul>

                    ${renderList(
                        careerSuggestions,
                        "No career suggestions available."
                    )}

                </ul>


                <!-- OLD IMPROVEMENTS -->

                <hr>

                <h3>💡 Basic Resume Suggestions</h3>

                <ul>

                    ${renderList(
                        data.improvements || [],
                        "No major improvements needed."
                    )}

                </ul>


                <!-- RESUME TEXT -->

                <hr>

                <details>

                    <summary>
                        📄 View Extracted Resume Text
                    </summary>

                    <pre>
${resumeText || "No text extracted."}
                    </pre>

                </details>

            </div>
        `;


    } catch (error) {

        console.error(
            "Resume Analysis Error:",
            error
        );


        message.innerHTML = `
            <p>
                ❌ Backend connection failed.
            </p>

            <small>
                Please check whether the Render backend is running.
            </small>
        `;
    }
}



// =========================================
// JOB MATCHER
// =========================================

async function checkJobMatch() {

    const jobInput =
        document.getElementById(
            "jobDescription"
        );


    const result =
        document.getElementById(
            "jobMatchResult"
        );


    const jobDescription =
        jobInput.value.trim();


    // =====================================
    // VALIDATION
    // =====================================

    if (!jobDescription) {

        result.innerHTML =
            "❌ Please enter a job description.";

        return;
    }


    if (!resumeText) {

        result.innerHTML =
            "❌ Please analyze your resume first.";

        return;
    }


    result.innerHTML = `
        <p>
            ⏳ AI is comparing your resume with the job...
        </p>
    `;


    try {

        const response =
            await fetch(
                `${API_URL}/job-match`,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        resume_skills:
                            resumeSkills,

                        resume_text:
                            resumeText,

                        job_description:
                            jobDescription,

                        resume_score:
                            window.resumeScore || 0
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            result.innerHTML =
                "❌ " +
                (
                    data.error ||
                    "Job matching failed."
                );

            return;
        }


        // =====================================
        // AI JOB ANALYSIS
        // =====================================

        const ai =
            data.ai_analysis || {};


        const aiSummary =
            ai.summary ||
            "AI job analysis is not available.";


        const aiStrengths =
            safeArray(ai.strengths);


        const aiWeaknesses =
            safeArray(ai.weaknesses);


        const aiMissingSkills =
            safeArray(ai.missing_skills);


        const aiImprovements =
            safeArray(ai.improvements);


        const aiInterview =
            safeArray(
                ai.interview_questions
            );


        const aiCareer =
            safeArray(
                ai.career_suggestions
            );


        // =====================================
        // DISPLAY JOB MATCH
        // =====================================

        result.innerHTML = `

            <div class="job-result">

                <hr>

                <h3>🎯 Job Match Result</h3>


                <h1>
                    ${data.match_percentage || 0}%
                </h1>


                <!-- MATCHED SKILLS -->

                <h4>✅ Matched Skills</h4>

                <p>

                    ${
                        data.matched_skills &&
                        data.matched_skills.length

                            ? data.matched_skills.join(
                                ", "
                            )

                            : "No matching skills found."
                    }

                </p>


                <!-- MISSING SKILLS -->

                <h4>❌ Missing Skills</h4>

                <p>

                    ${
                        data.missing_skills &&
                        data.missing_skills.length

                            ? data.missing_skills.join(
                                ", "
                            )

                            : "No major missing skills."
                    }

                </p>


                <!-- OLD RECOMMENDATIONS -->

                <h3>💡 Recommendations</h3>

                <ul>

                    ${renderList(
                        data.recommendations || [],
                        "No recommendations available."
                    )}

                </ul>


                <!-- ================================= -->
                <!-- AI JOB ANALYSIS -->
                <!-- ================================= -->

                <hr>

                <h2>🤖 AI Job Analysis</h2>


                <h3>🧠 AI Summary</h3>

                ${renderParagraph(
                    aiSummary
                )}


                <h3>💪 Your Strengths For This Job</h3>

                <ul>

                    ${renderList(
                        aiStrengths,
                        "No specific strengths identified."
                    )}

                </ul>


                <h3>⚠️ Areas To Improve</h3>

                <ul>

                    ${renderList(
                        aiWeaknesses,
                        "No major weaknesses identified."
                    )}

                </ul>


                <h3>📚 Skills You Should Learn</h3>

                <ul>

                    ${
                        aiMissingSkills.length
                            ? renderList(
                                aiMissingSkills
                            )
                            : (
                                data.missing_skills &&
                                data.missing_skills.length
                            )
                                ? renderList(
                                    data.missing_skills
                                )
                                : "<li>No major missing skills.</li>"
                    }

                </ul>


                <h3>💡 Personalized AI Improvements</h3>

                <ul>

                    ${renderList(
                        aiImprovements,
                        "No additional improvements available."
                    )}

                </ul>


                <h3>🎤 Interview Questions</h3>

                <ol>

                    ${
                        aiInterview.length

                            ? aiInterview
                                .map(
                                    question =>
                                        `<li>${question}</li>`
                                )
                                .join("")

                            : "<li>No interview questions generated.</li>"
                    }

                </ol>


                <h3>🎯 Career Suggestions</h3>

                <ul>

                    ${renderList(
                        aiCareer,
                        "No career suggestions available."
                    )}

                </ul>

            </div>

        `;


    } catch (error) {

        console.error(
            "Job Match Error:",
            error
        );


        result.innerHTML =
            "❌ Backend connection failed.";
    }
}