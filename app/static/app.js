const form = document.querySelector("#chatForm");
const input = document.querySelector("#messageInput");
const sendButton = document.querySelector("#sendButton");
const messages = document.querySelector("#messages");
const stateLabel = document.querySelector("#conversationState");
const resetButton = document.querySelector("#newConversation");
const voiceButton = document.querySelector("#voiceButton");
const voiceStatus = document.querySelector("#voiceStatus");

let conversationId = null;
let voiceConversationId = null;
let peerConnection = null;
let dataChannel = null;
let microphoneStream = null;

function appendMessage(role, text, type = "") {
  const item = document.createElement("div");
  item.className = `message ${role} ${type}`.trim();
  const speaker = document.createElement("span");
  speaker.className = "speaker";
  speaker.textContent = role === "user" ? "Vos" : "FerreBot";
  const paragraph = document.createElement("p");
  paragraph.textContent = text;
  item.append(speaker, paragraph);
  messages.append(item);
  messages.scrollTop = messages.scrollHeight;
}

async function sendMessage(text) {
  appendMessage("user", text);
  sendButton.disabled = true;
  input.disabled = true;

  try {
    const response = await fetch("/api/v1/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        message: text,
        conversation_id: conversationId,
        channel: "text",
      }),
    });
    const body = await response.json();
    if (!response.ok) {
      throw new Error(body.error?.message || "No se pudo procesar la consulta.");
    }

    conversationId = body.conversation_id;
    appendMessage("assistant", body.answer);
    stateLabel.textContent = `Intención: ${body.intent} · Estado: ${body.state}`;
  } catch (error) {
    appendMessage("assistant", error.message, "error");
  } finally {
    sendButton.disabled = false;
    input.disabled = false;
    input.focus();
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  await sendMessage(text);
});

document.querySelectorAll(".suggestions button").forEach((button) => {
  button.addEventListener("click", () => sendMessage(button.textContent));
});

resetButton.addEventListener("click", () => {
  conversationId = null;
  messages.innerHTML = "";
  appendMessage(
    "assistant",
    "Conversación reiniciada. ¿Qué producto o información necesitás?",
  );
  stateLabel.textContent = "Conversación nueva";
});

function getDemoUserId() {
  let value = localStorage.getItem("ferrebot_user_id");
  if (!value) {
    value = `web-${crypto.randomUUID()}`;
    localStorage.setItem("ferrebot_user_id", value);
  }
  return value;
}

async function executeRealtimeTool(item) {
  const response = await fetch("/api/v1/realtime/tool", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      conversation_id: voiceConversationId,
      name: item.name,
      arguments: JSON.parse(item.arguments || "{}"),
    }),
  });
  const body = await response.json();
  if (!response.ok) {
    throw new Error(body.error?.message || "Falló una herramienta de voz.");
  }
  voiceConversationId = body.conversation_id;

  dataChannel.send(JSON.stringify({
    type: "conversation.item.create",
    item: {
      type: "function_call_output",
      call_id: item.call_id,
      output: JSON.stringify(body.output),
    },
  }));
  dataChannel.send(JSON.stringify({type: "response.create"}));
}

async function handleRealtimeEvent(event) {
  const serverEvent = JSON.parse(event.data);
  if (serverEvent.type === "response.done") {
    const outputs = serverEvent.response?.output || [];
    for (const item of outputs) {
      if (item.type === "function_call") {
        try {
          await executeRealtimeTool(item);
        } catch (error) {
          voiceStatus.textContent = error.message;
        }
      }
    }
  }
  if (serverEvent.type === "input_audio_buffer.speech_started") {
    voiceStatus.textContent = "Te estoy escuchando…";
  }
  if (serverEvent.type === "response.created") {
    voiceStatus.textContent = "FerreBot está respondiendo…";
  }
  if (serverEvent.type === "error") {
    voiceStatus.textContent = serverEvent.error?.message || "Error de Realtime.";
  }
}

async function startVoice() {
  voiceStatus.hidden = false;
  voiceStatus.textContent = "Preparando la sesión de voz…";

  const configResponse = await fetch("/api/v1/realtime/config");
  const config = await configResponse.json();
  if (!config.enabled) {
    throw new Error(
      "La voz está preparada pero desactivada. Luego configuraremos la API key.",
    );
  }

  const tokenResponse = await fetch("/api/v1/realtime/token", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({user_id: getDemoUserId()}),
  });
  const tokenBody = await tokenResponse.json();
  if (!tokenResponse.ok) {
    throw new Error(tokenBody.error?.message || "No se pudo iniciar Realtime.");
  }

  const ephemeralKey = tokenBody.value;
  peerConnection = new RTCPeerConnection();
  const audio = document.createElement("audio");
  audio.autoplay = true;
  peerConnection.ontrack = (event) => {
    audio.srcObject = event.streams[0];
  };

  microphoneStream = await navigator.mediaDevices.getUserMedia({audio: true});
  peerConnection.addTrack(microphoneStream.getTracks()[0]);

  dataChannel = peerConnection.createDataChannel("oai-events");
  dataChannel.addEventListener("message", handleRealtimeEvent);
  dataChannel.addEventListener("open", () => {
    voiceStatus.textContent = "Voz conectada. Ya podés hablar.";
  });

  const offer = await peerConnection.createOffer();
  await peerConnection.setLocalDescription(offer);
  const sdpResponse = await fetch(
    "https://api.openai.com/v1/realtime/calls",
    {
      method: "POST",
      body: offer.sdp,
      headers: {
        Authorization: `Bearer ${ephemeralKey}`,
        "Content-Type": "application/sdp",
      },
    },
  );
  if (!sdpResponse.ok) {
    throw new Error("OpenAI no pudo completar la conexión WebRTC.");
  }
  await peerConnection.setRemoteDescription({
    type: "answer",
    sdp: await sdpResponse.text(),
  });

  voiceButton.classList.add("active");
  voiceButton.innerHTML = "<span aria-hidden='true'>■</span> Detener";
}

function stopVoice() {
  microphoneStream?.getTracks().forEach((track) => track.stop());
  dataChannel?.close();
  peerConnection?.close();
  microphoneStream = null;
  dataChannel = null;
  peerConnection = null;
  voiceButton.classList.remove("active");
  voiceButton.innerHTML = "<span aria-hidden='true'>🎙</span> Voz";
  voiceStatus.textContent = "Sesión de voz finalizada.";
}

voiceButton.addEventListener("click", async () => {
  if (peerConnection) {
    stopVoice();
    return;
  }
  try {
    await startVoice();
  } catch (error) {
    stopVoice();
    voiceStatus.hidden = false;
    voiceStatus.textContent = error.message;
  }
});

