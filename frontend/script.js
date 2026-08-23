let resumeSkills = [];


// =========================================
// RESUME ANALYZER
// =========================================

async function analyzeResume() {

    const fileInput = document.getElementById("resumeFile");
    const message = document.getElementById("message");

    if (!fileInput.files.length) {

        message.innerHTML =
            "❌ Please select a resume first.";

        return;
    }

    const file = fileInput.files[0];

    const formData = new FormData();

    formData.append("resume", file);

    message.innerHTML =
        "⏳ Analyzing your resume...";

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/analyze",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {

            message.innerHTML =
                "❌ " + (data.error || "Something went wrong.");

            return;
        }


        // Save skills for Job Matcher
        resumeSkills = data.skills || [];


        // Save resume score
        window.resumeScore = data.score
            ? data.score.total
            : 0;


        const contact = data.contact || {};


        const score = data.score || {

            total: 0,
            contact: 0,
            education: 0,
            skills: 0,
            experience: 0,
            projects: 0,
            objective: 0

        };


        message.innerHTML = `

            <h3>✅ Resume Analyzed</h3>


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


            <p>
                <strong>Skills:</strong>

                ${
                    data.skills && data.skills.length

                        ? data.skills.join(", ")

                        : "No skills detected"
                }

            </p>


            <hr>


            <h3>🎯 Resume Score</h3>

            <h2>${score.total}/100</h2>

            <h3>💡 Resume Improvement Suggestions</h3>

<ul>

    ${
        data.improvements &&
        data.improvements.length

            ? data.improvements
                .map(
                    item => `<li>${item}</li>`
                )
                .join("")

            : "<li>No major improvements needed.</li>"
    }

</ul>


            <p>
                Contact Information:
                ${score.contact}/10
            </p>


            <p>
                Education:
                ${score.education}/20
            </p>


            <p>
                Skills:
                ${score.skills}/20
            </p>


            <p>
                Experience:
                ${score.experience}/20
            </p>


            <p>
                Projects:
                ${score.projects}/20
            </p>


            <p>
                Objective:
                ${score.objective}/10
            </p>


            <hr>


            <h3>📄 Extracted Resume Text</h3>


            <pre>${data.text}</pre>

        `;


    } catch (error) {

        console.error(
            "Resume Analysis Error:",
            error
        );

        message.innerHTML =
            "❌ Backend se connection nahi ho pa raha.";
    }
}



// =========================================
// JOB MATCHER
// =========================================

async function checkJobMatch() {

    const jobDescription =
        document.getElementById("jobDescription").value;


    const result =
        document.getElementById("jobMatchResult");


    // Check job description
    if (!jobDescription.trim()) {

        result.innerHTML =
            "❌ Please enter a job description.";

        return;
    }


    // Check resume
    if (!resumeSkills.length) {

        result.innerHTML =
            "❌ Please analyze your resume first.";

        return;
    }


    result.innerHTML =
        "⏳ Checking job match...";


    try {

        const response = await fetch(
            "http://127.0.0.1:5000/job-match",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    resume_skills: resumeSkills,

                    job_description: jobDescription,

                    resume_score:
                        window.resumeScore || 0

                })

            }
        );


        const data = await response.json();


        if (!response.ok) {

            result.innerHTML =
                "❌ " +
                (
                    data.error ||
                    "Something went wrong."
                );

            return;
        }


        // =====================================
        // JOB MATCH RESULT
        // =====================================

        result.innerHTML = `

            <hr>


            <h3>🎯 Job Match</h3>


            <h2>
                ${data.match_percentage}%
            </h2>


            <h4>✅ Matched Skills</h4>


            <p>

                ${
                    data.matched_skills &&
                    data.matched_skills.length

                        ? data.matched_skills.join(", ")

                        : "No matching skills found"
                }

            </p>


            <h4>❌ Missing Skills</h4>


            <p>

                ${
                    data.missing_skills &&
                    data.missing_skills.length

                        ? data.missing_skills.join(", ")

                        : "No major missing skills"
                }

            </p>


            <hr>


            <h3>🤖 AI Recommendations</h3>


            <ul>

                ${
                    data.recommendations &&
                    data.recommendations.length

                        ? data.recommendations
                            .map(
                                recommendation =>
                                    `<li>${recommendation}</li>`
                            )
                            .join("")

                        : "<li>No recommendations available</li>"
                }

            </ul>

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