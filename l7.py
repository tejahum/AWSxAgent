@tool
def analyze_pr(diff_input: str) -> str:
    """
    Parses a raw unified-diff string and reconstructs each affected Python file’s full, updated source.
    Produces and returns a JSON string with exactly two keys:
      • "summary": a one-sentence description of the PR’s purpose
      • "files": a list of objects, each with:
          – "filename": the file’s path
          – "code": the cleaned, runnable Python source for that file
    Input: diff_input (raw unified-diff text)
    Output: JSON string as specified above
    """
    # implementation…
