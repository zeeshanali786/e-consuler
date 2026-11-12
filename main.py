from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, UTC
import uuid
from typing import Dict, List, Any, Optional

app = FastAPI(
    title="AI Relationship Counseling Engine",
    description="Production-ready backend API utilizing structural rolling profiles & asynchronous background cognitive parsing.",
    version="1.0.0"
)

class SessionInitResponse(BaseModel):
    couple_id: str = Field(..., description="Globally unique identifier for the couples' counseling session.")
    status: str = "initialized"

class ChatMessageInput(BaseModel):
    couple_id: str = Field(..., description="ID of the ongoing counseling session.")
    sender: str = Field(..., description="Identifier of the speaker (e.g., 'Husband', 'Wife').")
    message: str = Field(..., description="Raw chat content shared by the user.")

class ChatResponsePayload(BaseModel):
    counselor_response: str = Field(..., description="Empathetic reflective feedback generated from the counselor pipeline.")
    timestamp: datetime

class RollingProfileSchema(BaseModel):
    couple_id: str
    recurring_conflicts: List[str]
    agreed_homework: List[str]
    partner_a_triggers: List[str]
    partner_b_triggers: List[str]
    last_updated: Optional[datetime] = None

class CleanRelationshipDatabase:
    def __init__(self):
        self.rolling_profiles: Dict[str, Dict[str, Any]] = {}
        self.episodic_history: Dict[str, List[Dict[str, Any]]] = {}

    def get_profile(self, couple_id: str) -> Dict[str, Any]:
        if couple_id not in self.rolling_profiles:
            self.rolling_profiles[couple_id] = {
                "couple_id": couple_id,
                "recurring_conflicts": [],
                "agreed_homework": [],
                "partner_a_triggers": [],
                "partner_b_triggers": [],
                "last_updated": None
            }
        return self.rolling_profiles[couple_id]

    def update_profile(self, couple_id: str, updated_profile: Dict[str, Any]):
        updated_profile["last_updated"] = datetime.now(UTC)
        self.rolling_profiles[couple_id] = updated_profile

    def append_message(self, couple_id: str, sender: str, message: str):
        if couple_id not in self.episodic_history:
            self.episodic_history[couple_id] = []
        self.episodic_history[couple_id].append({
            "timestamp": datetime.now(UTC),
            "sender": sender,
            "message": message
        })

api_db = CleanRelationshipDatabase()

def background_extraction_task(couple_id: str, speaker: str, utterance: str):
    print(f"\n[Async Worker] Parsing entry from '{speaker}' in background...")
    current_profile = api_db.get_profile(couple_id)

    extracted_insights = {
        "detected_triggers": [],
        "new_conflicts": [],
        "new_agreements": []
    }

    lower_utterance = utterance.lower()
    if "upsets me when you" in lower_utterance or "bothers me when" in lower_utterance:
        trigger_phrase = utterance.split("when ")[-1].strip(".?! ")
        extracted_insights["detected_triggers"].append(trigger_phrase)
    if "argue about" in lower_utterance or "fight about" in lower_utterance:
        conflict_phrase = utterance.split("about ")[-1].strip(".?! ")
        extracted_insights["new_conflicts"].append(conflict_phrase)
    if "we should agree to" in lower_utterance or "we will try to" in lower_utterance:
        agreement_phrase = utterance.split("to ")[-1].strip(".?! ")
        extracted_insights["new_agreements"].append(agreement_phrase)

    if speaker.lower() in ["husband", "partner_a", "partner_1"]:
        current_profile["partner_a_triggers"] = list(set(current_profile["partner_a_triggers"] + extracted_insights["detected_triggers"]))
    else:
        current_profile["partner_b_triggers"] = list(set(current_profile["partner_b_triggers"] + extracted_insights["detected_triggers"]))

    current_profile["recurring_conflicts"] = list(set(current_profile["recurring_conflicts"] + extracted_insights["new_conflicts"]))
    current_profile["agreed_homework"] = list(set(current_profile["agreed_homework"] + extracted_insights["new_agreements"]))

    api_db.update_profile(couple_id, current_profile)
    print(f"[Async Worker] Database update committed successfully.")

@app.post("/session/start", response_model=SessionInitResponse, tags=["Session Management"])
async def start_session():
    new_id = f"couple_session_{uuid.uuid4().hex[:6]}"
    _ = api_db.get_profile(new_id)
    return SessionInitResponse(couple_id=new_id)

@app.post("/chat", response_model=ChatResponsePayload, tags=["Counseling Chat"])
async def post_message(payload: ChatMessageInput, background_tasks: BackgroundTasks):
    profile = api_db.get_profile(payload.couple_id)
    api_db.append_message(payload.couple_id, payload.sender, payload.message)
    background_tasks.add_task(background_extraction_task, payload.couple_id, payload.sender, payload.message)

    if profile["partner_a_triggers"] or profile["partner_b_triggers"]:
        trigger_item = profile["partner_a_triggers"][0] if payload.sender.lower() == "husband" else profile["partner_b_triggers"][0]
        counselor_response = f"[AI Counselor API]: I notice that trigger '{trigger_item}' is arising right now. Let's pause and reflect on how we can de-escalate this moment together."
    else:
        counselor_response = f"[AI Counselor API]: I hear you, {payload.sender}. Let's dive deeper into how this dynamic shows up in your relationship."

    return ChatResponsePayload(
        counselor_response=counselor_response,
        timestamp=datetime.now(UTC)
    )

@app.get("/profile/{couple_id}", response_model=RollingProfileSchema, tags=["Profile Metrics"])
async def get_couple_profile(couple_id: str):
    profile = api_db.get_profile(couple_id)
    if not profile or not profile.get("couple_id"):
        raise HTTPException(status_code=404, detail="Session profile not found")
    return profile
