from pathlib import Path
import tempfile, json
from analysis.generic import extract_input
from analysis.temperature import analyze_temperature_file
from rag.faiss_store import search_factory
from llm.groq_client import ask_json
from llm.prompts import SYSTEM, ANALYSIS
from database.repository import add_analysis, add_findings

def analyze_input(factory, analysis_type, uploaded_file, extra):
    suffix=Path(uploaded_file.name).suffix
    tmp=tempfile.NamedTemporaryFile(delete=False,suffix=suffix)
    tmp.write(uploaded_file.getbuffer()); tmp.close()

    if analysis_type=="Temperature Records":
        result=analyze_temperature_file(tmp.name, extra.get("min"), extra.get("max"))
        input_text=json.dumps(result,ensure_ascii=False)
    else:
        input_text=extract_input(tmp.name)
        result={"raw_input_preview":input_text[:5000]}

    query=f"{analysis_type}. What factory-specific requirements, limits, monitoring steps, verification steps and corrective actions are relevant?"
    context_chunks=search_factory(factory["id"],query,5)
    context="\n\n".join(
        f"[SOURCE: {c['document_name']} | page {c['page']}]\n{c['text']}" for c in context_chunks
    )
    prompt=ANALYSIS.format(factory=factory,input_text=input_text[:12000],context=context or "NO FACTORY-SPECIFIC SOURCE FOUND")
    ai=ask_json(SYSTEM,prompt)
    if analysis_type=="Temperature Records" and result.get("deviations"):
        ai.setdefault("findings",[])
        for d in result["deviations"]:
            ai["findings"].append({
                "title":"Temperature outside configured range",
                "category":"Temperature Control",
                "severity":"High",
                "evidence":f"Temperature record row {d['row']}: {d['temperature']}°C; configured range {extra.get('min')}–{extra.get('max')}°C.",
                "explanation":"The recorded value is outside the range supplied for this analysis.",
                "recommendation":"Investigate the deviation and follow the facility's corrective-action procedure."
            })
    aid=add_analysis(factory["id"],analysis_type,uploaded_file.name,"Completed",ai)
    findings=ai.get("findings",[]) if isinstance(ai,dict) else []
    add_findings(factory["id"],aid,findings)
    return ai, context_chunks
