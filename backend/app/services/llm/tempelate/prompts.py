class Prompts:
    @staticmethod
    def extract_jd_and_n(user_input: str) -> str:
        return f"""
    Analyze this user request: "{user_input}"

    Extract:
    1. The core Job Description (JD).
    2. The number of candidates requested (N). If not specified, default to 3.

    Respond ONLY in this exact format with nothing else:
    JD: [the job description text] | N: [number]
    """

    @staticmethod
    def evaluate_candidates(jd_text: str, top_n: int, context_docs: str) -> str:
        return f"""
    You are a professional HR Recruiter. Your task is to evaluate candidates for the following job.
    JOB DESCRIPTION: {jd_text}
    NUMBER OF POSITIONS: {top_n}
    CANDIDATE CVs FROM DATABASE:
    {context_docs}

    INSTRUCTIONS:
    - Select the top {top_n} candidates
    - Ranks all {top_n} candidates from most to least suitable
    - Use the candidate's REAL NAME from their CV (not A, B, or numbers)
    - For each candidate provide:
    1. Full Name
    2. For each candidate explains: why they fit, their key strengths, and any gaps 
    3. Top 3 matching skills
    4. End with a final hiring recommendation

    OUTPUT FORMAT (follow this exactly):
    Rank 1: [Full Name]
    - Why they fit: ...
    - Key strengths: ...
    - Gaps: ...
    - Top skills: skill1, skill2, skill3

    Rank 2: [Full Name]
    - Why they fit: ...
    - Key strengths: ...
    - Gaps: ...
    - Top skills: skill1, skill2, skill3

    My Personal Recommendation:
    As an HR professional, I strongly recommend [name] because [specific reason based on the analysis above].
    """
