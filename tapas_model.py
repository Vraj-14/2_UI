# # import re
# # import pandas as pd
# # from transformers import TapasTokenizer, TapasForQuestionAnswering
# # from app.config import TAPAS_MODEL

# # # Load TAPAS
# # tapas_tokenizer = TapasTokenizer.from_pretrained(TAPAS_MODEL)
# # tapas_model = TapasForQuestionAnswering.from_pretrained(TAPAS_MODEL)

# # # === Heuristic: Is it a table query? ===
# # def is_table_query(question):
# #     keywords = ["rate", "growth", "%", "total", "sum", "revenue", "profit", "cost", "change", "difference", "increase", "decrease","Name of the Company", "Company Name", "Company","Nature of transactions with struck off Company",
# #                 "Transactions during the year March 31, 2024","Balance Outstanding as on March 31, 2024", "Balance Outstanding as on March 31, 2023", "Balance Outstanding as on March 31, 2022", "Balance Outstanding as on March 31, 2021", "Balance Outstanding as on March 31, 2020",
# #                 "Relationship with the Struck off Company"]
# #     return any(k.lower() in question.lower() for k in keywords)

# # # === Heuristic: Select best table match ===
# # def select_table_by_title(tables, question):
# #     q_norm = re.sub(r"[^a-z0-9]", "", question.lower())
# #     for t in tables:
# #         t_norm = re.sub(r"[^a-z0-9]", "", t["title"].lower())
# #         if t_norm in q_norm:
# #             return t
# #     return tables[0]

# # # === Convert markdown to DataFrame ===
# # from io import StringIO
# # def markdown_to_dataframe(markdown_table):
# #     # Remove alignment row and pipes
# #     cleaned = "\n".join(
# #         line for i, line in enumerate(markdown_table.strip().splitlines())
# #         if i != 1 and line.strip().startswith("|")
# #     )
# #     try:
# #         df = pd.read_csv(StringIO(cleaned), sep="|", engine="python")
# #         df = df.dropna(axis=1, how='all')
# #         df.columns = df.columns.astype(str)
# #         return df
# #     except Exception as e:
# #         print(f"[TAPAS] Error parsing markdown:\n{e}")
# #         return pd.DataFrame()

# # # === TAPAS QA ===
# # def tapas_answer(df, question):
# #     if df.empty:
# #         return "No valid table found."
# #     inputs = tapas_tokenizer(table=df, queries=[question], return_tensors="pt")
# #     outputs = tapas_model(**inputs)
# #     answers, _ = tapas_tokenizer.convert_logits_to_predictions(
# #         inputs,
# #         outputs.logits.detach(),
# #         outputs.logits_aggregation.detach()
# #     )
# #     selected_cells = answers[0]
# #     extracted = []
# #     for row, col in selected_cells:
# #         if row < df.shape[0] and col < df.shape[1]:
# #             extracted.append(df.iat[row, col])
# #     return ", ".join(extracted) if extracted else "No relevant answer found."

# import re
# import pandas as pd
# from transformers import TapasTokenizer, TapasForQuestionAnswering
# from app.config import TAPAS_MODEL

# # Load TAPAS
# tapas_tokenizer = TapasTokenizer.from_pretrained(TAPAS_MODEL)
# tapas_model = TapasForQuestionAnswering.from_pretrained(TAPAS_MODEL)

# # === Heuristic: Is it a table query? ===
# def is_table_query(question):
#     keywords = [
#         "rate", "growth", "%", "total", "sum", "revenue", "profit", "cost","Age","Salary",
#         "change", "difference", "increase", "decrease", "Name of the Company",
#         "Company Name", "Company", "Nature of transactions with struck off Company",
#         "Transactions during the year March 31, 2024",
#         "Balance Outstanding as on March 31, 2024",
#         "Balance Outstanding as on March 31, 2023",
#         "Balance Outstanding as on March 31, 2022",
#         "Balance Outstanding as on March 31, 2021",
#         "Balance Outstanding as on March 31, 2020",
#         "Relationship with the Struck off Company"
#     ]
#     return any(k.lower() in question.lower() for k in keywords)

# # === Heuristic: Select best table match ===
# def select_table_by_title(tables, question):
#     q_norm = re.sub(r"[^a-z0-9]", "", question.lower())
#     for t in tables:
#         t_norm = re.sub(r"[^a-z0-9]", "", t["title"].lower())
#         if t_norm in q_norm:
#             return t
#     return tables[0]

# # === Convert markdown to DataFrame ===
# from io import StringIO
# def markdown_to_dataframe(markdown_table):
#     # Remove alignment row and pipes
#     cleaned = "\n".join(
#         line for i, line in enumerate(markdown_table.strip().splitlines())
#         if i != 1 and line.strip().startswith("|")
#     )
#     try:
#         df = pd.read_csv(StringIO(cleaned), sep="|", engine="python")
#         df = df.dropna(axis=1, how='all')
#         df.columns = df.columns.astype(str)
#         return df
#     except Exception as e:
#         print(f"[TAPAS] Error parsing markdown:\n{e}")
#         return pd.DataFrame()

# # === Preprocess table: Fix NaNs & convert all cells to strings ===
# def preprocess_table(df):
#     df = df.fillna("")
#     df = df.astype(str)
#     return df

# # === TAPAS QA ===
# # def tapas_answer(df, question):
# #     if df.empty:
# #         return "No valid table found."
    
# #     df = preprocess_table(df)  # 🧠 Fix: Ensure all cells are strings
    
# #     inputs = tapas_tokenizer(table=df, queries=[question], return_tensors="pt")
# #     outputs = tapas_model(**inputs)
    
# #     answers, _ = tapas_tokenizer.convert_logits_to_predictions(
# #         inputs,
# #         outputs.logits.detach(),
# #         outputs.logits_aggregation.detach()
# #     )
    
# #     selected_cells = answers[0]
# #     extracted = []
# #     for row, col in selected_cells:
# #         if row < df.shape[0] and col < df.shape[1]:
# #             extracted.append(df.iat[row, col])
    
# #     return ", ".join(extracted) if extracted else "No relevant answer found."/
# def tapas_answer(df, question):
#     if df.empty:
#         return "No valid table found."

#     df = preprocess_table(df)
#     inputs = tapas_tokenizer(table=df, queries=[question], return_tensors="pt")
#     outputs = tapas_model(**inputs)

#     answers, _ = tapas_tokenizer.convert_logits_to_predictions(
#         inputs,
#         outputs.logits.detach(),
#         outputs.logits_aggregation.detach()
#     )

#     selected_cells = answers[0]
#     extracted = []
#     for row, col in selected_cells:
#         if row < df.shape[0] and col < df.shape[1]:
#             extracted.append(df.iat[row, col])

#     if not extracted:
#         return "No relevant answer found."

#     # 👉 If question contains "sum", try computing the numeric sum
#     if "sum" in question.lower():
#         try:
#             numeric_vals = [float(str(x).replace(",", "")) for x in extracted if re.match(r"^\d+(\.\d+)?$", str(x).replace(",", ""))]
#             return f"{sum(numeric_vals):,.2f}"
#         except Exception as e:
#             return f"Found values: {', '.join(extracted)} (⚠️ sum failed: {e})"

#     return ", ".join(extracted)




#----------------------------------------------------------------------------------------------------------------------------
# # WITH SUM, AVG, MIN, MAX, PERCENTAGE SUPPORT

# import re
# import pandas as pd
# from transformers import TapasTokenizer, TapasForQuestionAnswering
# from app.config import TAPAS_MODEL
# from io import StringIO

# # Load TAPAS model
# tapas_tokenizer = TapasTokenizer.from_pretrained(TAPAS_MODEL)
# tapas_model = TapasForQuestionAnswering.from_pretrained(TAPAS_MODEL)

# # === Heuristic: Table Query Detection ===
# def is_table_query(question):
#     keywords = [
#         "rate", "growth", "%", "total", "sum", "average", "mean", "min", "max", "minimum", "maximum", "revenue", "profit", "cost",
#         "change", "difference", "increase", "decrease", "Name of the Company", "Company Name", "Company",
#         "Age", "Salary", "EstimatedSalary", "Nature of transactions", "Outstanding","No. of Shares as on March 31, 2024",
#         "Transactions during the year March 31, 2024", "Balance Outstanding as on March 31, 2024",
#         "Balance Outstanding as on March 31, 2023", "Balance Outstanding as on","Nature of transactions with struck off Company",
#         "Balance Outstanding as on March 31, 2022", "Balance Outstanding as on March 31, 2021",
#         "Name of the Company","Relationship with the Struck off Company"]
#     return any(k.lower() in question.lower() for k in keywords)

# # === Table title matcher ===
# def select_table_by_title(tables, question):
#     q_norm = re.sub(r"[^a-z0-9]", "", question.lower())
#     for t in tables:
#         t_norm = re.sub(r"[^a-z0-9]", "", t["title"].lower())
#         if t_norm in q_norm:
#             return t
#     return tables[0]

# # === Markdown to DataFrame ===
# def markdown_to_dataframe(markdown_table):
#     cleaned = "\n".join(
#         line for i, line in enumerate(markdown_table.strip().splitlines())
#         if i != 1 and line.strip().startswith("|")
#     )
#     try:
#         df = pd.read_csv(StringIO(cleaned), sep="|", engine="python")
#         df = df.dropna(axis=1, how="all")
#         df.columns = df.columns.astype(str)
#         return df
#     except Exception as e:
#         print(f"[TAPAS] Error parsing markdown:\n{e}")
#         return pd.DataFrame()

# # === Clean & prepare table ===
# def preprocess_table(df):
#     df = df.fillna("")
#     df = df.astype(str)
#     return df

# # === Main TAPAS Answer Function with aggregations ===
# def tapas_answer(df, question):
#     if df.empty:
#         return "No valid table found."

#     df = preprocess_table(df)

#     inputs = tapas_tokenizer(table=df, queries=[question], return_tensors="pt")
#     outputs = tapas_model(**inputs)

#     answers, _ = tapas_tokenizer.convert_logits_to_predictions(
#         inputs,
#         outputs.logits.detach(),
#         outputs.logits_aggregation.detach()
#     )

#     selected_cells = answers[0]
#     extracted = []
#     for row, col in selected_cells:
#         if row < df.shape[0] and col < df.shape[1]:
#             extracted.append(df.iat[row, col])

#     if not extracted:
#         return "No relevant answer found."

#     # === Try numeric extraction ===
#     def to_float(x):
#         try:
#             return float(str(x).replace(",", "").replace("₹", "").replace("%", "").strip())
#         except:
#             return None

#     numeric_vals = list(filter(None, [to_float(x) for x in extracted]))

#     q_lower = question.lower()

#     # SUM
#     if "sum" in q_lower or "total" in q_lower:
#         if numeric_vals:
#             return f"Sum: {sum(numeric_vals):,.2f}"
#     # AVERAGE
#     elif "average" in q_lower or "mean" in q_lower:
#         if numeric_vals:
#             return f"Average: {sum(numeric_vals)/len(numeric_vals):,.2f}"
#     # MIN
#     elif "min" in q_lower or "minimum" in q_lower:
#         if numeric_vals:
#             return f"Minimum: {min(numeric_vals):,.2f}"
#     # MAX
#     elif "max" in q_lower or "maximum" in q_lower:
#         if numeric_vals:
#             return f"Maximum: {max(numeric_vals):,.2f}"
#     # PERCENTAGE
#     elif "%" in q_lower or "percent" in q_lower or "percentage" in q_lower:
#         if numeric_vals:
#             return f"Percentage value(s): {', '.join(f'{v:.2f}%' for v in numeric_vals)}"

#     return ", ".join(extracted)



# ------------------------------------------------------------------------------------------------------------------
# # INLCUDING CONTENT MATCING FOR TABLES 

# # tapas_model.py - Enhanced with table content-based selection and row filtering

# import re
# import pandas as pd
# from transformers import TapasTokenizer, TapasForQuestionAnswering
# from app.config import TAPAS_MODEL
# from io import StringIO

# # === Load TAPAS ===
# tapas_tokenizer = TapasTokenizer.from_pretrained(TAPAS_MODEL)
# tapas_model = TapasForQuestionAnswering.from_pretrained(TAPAS_MODEL)

# # === Detect Table Queries ===
# def is_table_query(question):
#     keywords = [
#         "rate", "growth", "%", "total", "sum", "average", "mean", "min", "max", "minimum", "maximum",
#         "revenue", "profit", "cost", "change", "difference", "increase", "decrease",
#         "Age", "Salary", "EstimatedSalary", "No. of Shares as on March 31, 2024",
#         "Name of the Company", "Company Name", "Company", "Outstanding",
#         "Nature of transactions", "Relationship with the Struck off Company"
#     ]
#     return any(k.lower() in question.lower() for k in keywords)

# # === Table selection based on question-content similarity ===
# def select_table_by_content(tables, question):
#     q_norm = re.sub(r"[^a-z0-9]", "", question.lower())
#     best_match = tables[0]
#     max_score = 0

#     for t in tables:
#         content = t["title"] + " " + t["table"]
#         content_norm = re.sub(r"[^a-z0-9]", "", content.lower())
#         score = sum(1 for word in q_norm.split() if word in content_norm)
#         if score > max_score:
#             best_match = t
#             max_score = score

#     return best_match

# # === Convert markdown table to DataFrame ===
# def markdown_to_dataframe(markdown_table):
#     cleaned = "\n".join(
#         line for i, line in enumerate(markdown_table.strip().splitlines())
#         if i != 1 and line.strip().startswith("|")
#     )
#     try:
#         df = pd.read_csv(StringIO(cleaned), sep="|", engine="python")
#         df = df.dropna(axis=1, how="all")
#         df.columns = df.columns.astype(str)
#         return df
#     except Exception as e:
#         print(f"[TAPAS] Error parsing markdown:\n{e}")
#         return pd.DataFrame()

# # === Clean DataFrame ===
# def preprocess_table(df):
#     df = df.fillna("")
#     df = df.astype(str)
#     return df

# # === Main TAPAS Answering Logic ===
# def tapas_answer(df, question):
#     if df.empty:
#         return "No valid table found."

#     df = preprocess_table(df)

#     # Step 1: Try to detect row-filter condition
#     matched_rows = df.copy()
#     for col in df.columns:
#         # Check if any cell in this column is present in question
#         matched = df[col].apply(lambda x: str(x).lower() in question.lower())
#         if matched.any():
#             matched_rows = df[matched]
#             break  # stop at first matching column

#     # If no match, fallback to original table
#     if matched_rows.empty:
#         matched_rows = df

#     inputs = tapas_tokenizer(table=matched_rows, queries=[question], return_tensors="pt")
#     outputs = tapas_model(**inputs)

#     answers, _ = tapas_tokenizer.convert_logits_to_predictions(
#         inputs,
#         outputs.logits.detach(),
#         outputs.logits_aggregation.detach()
#     )

#     selected_cells = answers[0]
#     extracted = []
#     for row, col in selected_cells:
#         if row < matched_rows.shape[0] and col < matched_rows.shape[1]:
#             extracted.append(matched_rows.iat[row, col])

#     if not extracted:
#         return "No relevant answer found."

#     # === Try numeric extraction ===
#     def to_float(x):
#         try:
#             return float(str(x).replace(",", "").replace("₹", "").replace("%", "").strip())
#         except:
#             return None

#     numeric_vals = list(filter(None, [to_float(x) for x in extracted]))
#     q_lower = question.lower()

#     if "sum" in q_lower or "total" in q_lower:
#         if numeric_vals:
#             return f"Sum: {sum(numeric_vals):,.2f}"
#     elif "average" in q_lower or "mean" in q_lower:
#         if numeric_vals:
#             return f"Average: {sum(numeric_vals)/len(numeric_vals):,.2f}"
#     elif "min" in q_lower or "minimum" in q_lower:
#         if numeric_vals:
#             return f"Minimum: {min(numeric_vals):,.2f}"
#     elif "max" in q_lower or "maximum" in q_lower:
#         if numeric_vals:
#             return f"Maximum: {max(numeric_vals):,.2f}"
#     elif "%" in q_lower or "percent" in q_lower or "percentage" in q_lower:
#         if numeric_vals:
#             return f"Percentage value(s): {', '.join(f'{v:.2f}%' for v in numeric_vals)}"

#     return ", ".join(extracted)



# -------------------------------------------------------------------------------------------

import re
import pandas as pd
from transformers import TapasTokenizer, TapasForQuestionAnswering
from app.config import TAPAS_MODEL
from io import StringIO

# Load TAPAS model
tapas_tokenizer = TapasTokenizer.from_pretrained(TAPAS_MODEL)
tapas_model = TapasForQuestionAnswering.from_pretrained(TAPAS_MODEL)

# === Heuristic: Table Query Detection ===
def is_table_query(question):
    keywords = [
        "rate", "growth", "%", "total", "sum", "average", "mean", "min", "max", "minimum", "maximum", "revenue", "profit", "cost",
        "change", "difference", "increase", "decrease", "Name of the Company", "Company Name", "Company",
        "Age", "Salary", "EstimatedSalary", "Nature of transactions", "Outstanding", "No. of Shares as on March 31, 2024",
        "Transactions during the year March 31, 2024", "Balance Outstanding as on March 31, 2024",
        "Balance Outstanding as on March 31, 2023", "Balance Outstanding as on", "Nature of transactions with struck off Company",
        "Balance Outstanding as on March 31, 2022", "Balance Outstanding as on March 31, 2021",
        "Relationship with the Struck off Company"
    ]
    return any(k.lower() in question.lower() for k in keywords)

# === Table title matcher (fallback: first table) ===
def select_table_by_title(tables, question):
    q_norm = re.sub(r"[^a-z0-9]", "", question.lower())
    for t in tables:
        t_norm = re.sub(r"[^a-z0-9]", "", t["title"].lower())
        if t_norm in q_norm:
            return t
    return tables[0]

# === Table content matcher (fuzzy match) ===
def select_table_by_content(tables, question):
    matches = [t for t in tables if any(word in t['table'].lower() for word in question.lower().split())]
    return matches[0] if matches else tables[0]

# === Markdown to DataFrame ===
def markdown_to_dataframe(markdown_table):
    cleaned = "\n".join(
        line for i, line in enumerate(markdown_table.strip().splitlines())
        if i != 1 and line.strip().startswith("|")
    )
    try:
        df = pd.read_csv(StringIO(cleaned), sep="|", engine="python")
        df = df.dropna(axis=1, how="all")
        df.columns = df.columns.astype(str)
        return df
    except Exception as e:
        print(f"[TAPAS] Error parsing markdown:\n{e}")
        return pd.DataFrame()

# === Clean & prepare table ===
def preprocess_table(df):
    df = df.fillna("")
    df = df.astype(str)
    return df

# === Main TAPAS Answer Function with aggregations ===
def tapas_answer(df, question):
    if df.empty:
        return "No valid table found."

    df = preprocess_table(df)

    inputs = tapas_tokenizer(table=df, queries=[question], return_tensors="pt")
    outputs = tapas_model(**inputs)

    answers, _ = tapas_tokenizer.convert_logits_to_predictions(
        inputs,
        outputs.logits.detach(),
        outputs.logits_aggregation.detach()
    )

    selected_cells = answers[0]
    extracted = []
    for row, col in selected_cells:
        if row < df.shape[0] and col < df.shape[1]:
            extracted.append(df.iat[row, col])
        else:
            print(f"[⚠️ TAPAS] Ignored out-of-bounds cell: ({row}, {col})")

    if not extracted:
        return "No relevant answer found."

    # === Try numeric extraction ===
    def to_float(x):
        try:
            return float(str(x).replace(",", "").replace("₹", "").replace("%", "").strip())
        except:
            return None

    numeric_vals = list(filter(None, [to_float(x) for x in extracted]))
    q_lower = question.lower()

    if "sum" in q_lower or "total" in q_lower:
        if numeric_vals:
            return f"Sum: {sum(numeric_vals):,.2f}"
    elif "average" in q_lower or "mean" in q_lower:
        if numeric_vals:
            return f"Average: {sum(numeric_vals)/len(numeric_vals):,.2f}"
    elif "min" in q_lower or "minimum" in q_lower:
        if numeric_vals:
            return f"Minimum: {min(numeric_vals):,.2f}"
    elif "max" in q_lower or "maximum" in q_lower:
        if numeric_vals:
            return f"Maximum: {max(numeric_vals):,.2f}"
    elif "%" in q_lower or "percent" in q_lower or "percentage" in q_lower:
        if numeric_vals:
            return f"Percentage(s): {', '.join(f'{v:.2f}%' for v in numeric_vals)}"

    return ", ".join(extracted)
