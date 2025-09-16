import requests
import os

OPENAI_KEY = "KEYACCESS"

# Store your HTML template as a big Python string
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title><!-- AI: Insert Name Here -->Resume</title>
  <link rel="stylesheet" href="/apple_style.css" />
</head>
<body>
  <div class="container">
    <header>
      <!-- AI: Insert Name Here -->
      <h1><!-- Name --></h1>
      <!-- AI: Insert Subtitle (e.g., Profession, Certifications) -->
      <p class="subtitle"><!-- Subtitle --></p>
      <!-- AI: Insert Contact Info (Location, Email, LinkedIn, etc.) -->
      <p class="contact"><!-- Contact Info --></p>
    </header>

    <section>
      <h2>Professional Summary</h2>
      <!-- AI: Insert Professional Summary Paragraph -->
      <p><!-- Professional summary --></p>
    </section>

    <section>
      <h2>Core Competencies</h2>
      <!-- AI: List Core Competencies/Skills -->
      <ul>
        <!-- <li>Skill/Competency</li> -->
      </ul>
    </section>

    <section>
      <h2>Key Achievements & Strengths</h2>
      <!-- AI: List Key Achievements/Strengths -->
      <ul>
        <!-- <li><strong>Label:</strong> Description</li> -->
      </ul>
    </section>

    <section>
      <h2>Certifications</h2>
      <!-- AI: List Certifications -->
      <ul>
        <!-- <li><strong>Certification Name</strong> – Details</li> -->
      </ul>
    </section>

    <section>
      <h2>Professional Experience</h2>
      <!-- AI: List Professional Experience as <article> blocks -->
      <!--
      <article>
        <h3>Job Title<br/><span>Year(s), Organization, Location</span></h3>
      </article>
      -->
    </section>

    <section>
      <h2>Consulting History</h2>
      <!-- AI: List Consulting, Research, or Additional Experience -->
      <!--
      <article>
        <h3>Role/Title<br/><span>Year(s), Organization/Details</span></h3>
      </article>
      -->
    </section>

    <section>
      <h2>Education</h2>
      <!-- AI: List Education History -->
      <ul>
        <!-- <li><strong>Degree</strong>, Institution — Year (Notes)</li> -->
      </ul>
    </section>

    <section>
      <h2>Cover Letter Statement</h2>
      <!-- AI: Insert personalized, first-person cover letter statement using only resume info. No embellishment. Sign with the candidate's name if available. -->
      <p><!-- Cover letter paragraph(s) --></p>
      <p><strong>Warm regards,</strong><br/><!-- Signature (Name) --></p>
    </section>

  </div>
</body>
</html>
"""

def txt_to_html_resume(txt_path, api_key=OPENAI_KEY, temperature=0.05, max_tokens=2500):
    with open(txt_path, "r", encoding="utf-8") as f:
        resume_txt = f.read()

    prompt = (
          "You are an expert resume parser and writer. "
    "Using the provided HTML template, fill ONLY the areas marked <!-- AI: ... --> and related comment blocks with content found directly in the resume text. "
    "Do NOT invent or embellish. If data is missing, leave that field blank."
    "For the 'Cover Letter Statement' section at the end, write a very brief, first-person (I/me/my) cover letter using only details from the resume. "
    "Highlight the person's most recent roles and best personality traits, if these are mentioned in the resume, but do NOT add any new information. "
    "The cover letter should sound as if written by the candidate and end with a signature using the candidate's name if found. "
    "Return ONLY a valid HTML document, keeping all structure and comments unchanged except where fields are replaced with resume content."
    "\n\nHTML TEMPLATE:\n"
    f"{HTML_TEMPLATE}\n\n"
    "RESUME TEXT:\n"
    f"{resume_txt}"
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4.1-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}
                ]
            }
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        html_resume = response.json()["choices"][0]["message"]["content"]
        return html_resume.strip()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    txt_filename = os.path.join(base_dir, "resumes", "resumeTXT", "ChristineDeLuca.txt")
    if not os.path.exists(txt_filename):
        print(f"ERROR: {txt_filename} not found. Please put your resume text in this file.")
        exit(1)

    try:
        html_output = txt_to_html_resume(txt_filename)
        # Print or save to file
        print(html_output)
        # Optionally, write the result to HTML file:
        html_outfile = os.path.splitext(txt_filename)[0] + ".html"
        with open(html_outfile, "w", encoding="utf-8") as outf:
            outf.write(html_output)
    except Exception as e:
        print(e)
