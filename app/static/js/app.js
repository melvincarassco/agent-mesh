document.addEventListener("DOMContentLoaded", () => {
    const workflowForm = document.getElementById("workflowForm");
    const goalInput = document.getElementById("goalInput");
    const launchBtn = document.getElementById("launchBtn");
    const launchSpinner = document.getElementById("launchSpinner");
    const systemStatus = document.getElementById("systemStatus");
    const statusLabel = systemStatus.querySelector(".status-label");
    const dagContainer = document.getElementById("dagContainer");
    const dagEmptyState = document.getElementById("dagEmptyState");
    const progressBar = document.getElementById("progressBar");
    const consoleBody = document.getElementById("consoleBody");
    const workflowIdBadge = document.getElementById("workflowIdBadge");
    const clearConsoleBtn = document.getElementById("clearConsoleBtn");
    const presetBtns = document.querySelectorAll(".preset-btn");

    let activeEventSource = null;
    let totalTasks = 0;
    let completedTasks = 0;

    // Agent icons lookup map
    const AGENT_ICONS = {
        planner: "🧠",
        researcher: "🔍",
        executor: "⚡",
        critic: "⚖️"
    };

    // Preset Goal Handlers
    presetBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            goalInput.value = btn.dataset.goal;
        });
    });

    // Clear Console Handler
    clearConsoleBtn.addEventListener("click", () => {
        consoleBody.innerHTML = `
            <div class="console-line system-line">
                <span class="timestamp">[SYSTEM]</span> Console cleared. Waiting for event stream...
            </div>
        `;
    });

    // Workflow Submission Form
    workflowForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const goal = goalInput.value.trim();
        if (!goal) return;

        // Reset UI state
        setSubmittingState(true);
        logConsole("[SUBMIT]", `Submitting goal: "${goal}"`, "system-line");

        try {
            const response = await fetch("/v1/workflows/submit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ goal })
            });

            if (!response.ok) throw new Error(`HTTP Error ${response.status}`);

            const data = await response.json();
            const workflowId = data.workflow_id;
            
            workflowIdBadge.textContent = workflowId;
            logConsole("[DAG]", `Workflow Initialized (${workflowId})`, "event-started");

            // Close existing EventSource if active
            if (activeEventSource) activeEventSource.close();

            // Connect to SSE Endpoint
            connectSSEStream(workflowId);

        } catch (err) {
            logConsole("[ERROR]", `Failed to initialize workflow: ${err.message}`, "event-error");
            setSubmittingState(false);
        }
    });

    function connectSSEStream(workflowId) {
        setSystemStatus("Executing Agent Mesh...", true);
        const sseUrl = `/v1/workflows/${workflowId}/stream`;
        activeEventSource = new EventSource(sseUrl);

        activeEventSource.onmessage = (e) => {
            try {
                const eventData = JSON.parse(e.data);
                handleSSEEvent(eventData);
            } catch (err) {
                console.error("Failed to parse SSE payload", err);
            }
        };

        activeEventSource.onerror = (err) => {
            logConsole("[SSE]", "EventSource connection closed.", "system-line");
            activeEventSource.close();
            setSubmittingState(false);
            setSystemStatus("System Online", false);
        };
    }

    function handleSSEEvent(data) {
        const timestamp = new Date().toLocaleTimeString();

        switch (data.event) {
            case "workflow_started":
                logConsole(`[${timestamp}]`, `Workflow Started: ${data.plan_summary}`, "event-started");
                fetchDAGGraph(data.workflow_id);
                break;

            case "task_started":
                logConsole(`[${timestamp}]`, `Task Started [${data.task_id}]: Assigned to ${data.agent}`, "event-started");
                updateNodeStatus(data.task_id, "running");
                break;

            case "task_completed":
                logConsole(`[${timestamp}]`, `Task Completed [${data.task_id}]: ${JSON.stringify(data.output)}`, "event-completed");
                updateNodeStatus(data.task_id, "completed", data.output);
                completedTasks++;
                updateProgressBar();
                break;

            case "task_failed":
                logConsole(`[${timestamp}]`, `Task Failed [${data.task_id}]: ${data.error}`, "event-error");
                updateNodeStatus(data.task_id, "failed");
                break;

            case "workflow_finished":
                logConsole(`[${timestamp}]`, `Workflow Finished with status: ${data.final_status}`, "event-finished");
                setSubmittingState(false);
                setSystemStatus("System Online", false);
                if (activeEventSource) activeEventSource.close();
                break;
        }
    }

    async function fetchDAGGraph(workflowId) {
        try {
            const res = await fetch(`/v1/workflows/${workflowId}`);
            if (!res.ok) return;
            const data = await res.json();
            
            const nodes = data.graph.nodes;
            totalTasks = Object.keys(nodes).length;
            completedTasks = 0;
            updateProgressBar();

            renderDAGNodes(nodes);
        } catch (err) {
            console.error("Failed to fetch DAG graph", err);
        }
    }

    function renderDAGNodes(nodes) {
        if (dagEmptyState) dagEmptyState.remove();
        dagContainer.innerHTML = "";

        Object.values(nodes).forEach(node => {
            const icon = AGENT_ICONS[node.assigned_agent] || "🤖";
            const card = document.createElement("div");
            card.className = `task-node-card status-${node.status.toLowerCase()}`;
            card.id = `node-${node.id}`;

            card.innerHTML = `
                <div class="node-left">
                    <div class="agent-icon">${icon}</div>
                    <div>
                        <div class="node-title">${node.title}</div>
                        <div class="node-desc">${node.description}</div>
                    </div>
                </div>
                <span class="node-status-tag status-${node.status.toLowerCase()}">${node.status}</span>
            `;
            dagContainer.appendChild(card);
        });
    }

    function updateNodeStatus(taskId, status, outputData = null) {
        const nodeCard = document.getElementById(`node-${taskId}`);
        if (!nodeCard) return;

        nodeCard.className = `task-node-card ${status}`;
        const tag = nodeCard.querySelector(".node-status-tag");
        if (tag) {
            tag.className = `node-status-tag status-${status}`;
            tag.textContent = status.toUpperCase();
        }
    }

    function updateProgressBar() {
        if (totalTasks === 0) {
            progressBar.style.width = "0%";
            return;
        }
        const pct = Math.round((completedTasks / totalTasks) * 100);
        progressBar.style.width = `${pct}%`;
    }

    function logConsole(prefix, text, className = "") {
        const line = document.createElement("div");
        line.className = `console-line ${className}`;
        line.innerHTML = `<span class="timestamp">${prefix}</span> ${escapeHtml(text)}`;
        consoleBody.appendChild(line);
        consoleBody.scrollTop = consoleBody.scrollHeight;
    }

    function setSubmittingState(isSubmitting) {
        launchBtn.disabled = isSubmitting;
        if (isSubmitting) {
            launchSpinner.classList.remove("hidden");
        } else {
            launchSpinner.classList.add("hidden");
        }
    }

    function setSystemStatus(label, isExecuting) {
        statusLabel.textContent = label;
        if (isExecuting) {
            systemStatus.style.borderColor = "rgba(6, 182, 212, 0.5)";
        } else {
            systemStatus.style.borderColor = "rgba(16, 185, 129, 0.3)";
        }
    }

    function escapeHtml(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }
});
