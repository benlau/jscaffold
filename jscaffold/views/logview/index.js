
class LogViewState {
    constructor(container) {
        this.container = container;
        this.timer = undefined
        this.startTime = 0;
    }

    onStartProcessing() {
        if (this.timer) {
            clearInterval(this.timer);
        }

        this.startTime = Date.now();

        this.timer = setInterval(() => {
            const elapsed = Math.round((Date.now() - this.startTime) / 1000);
            this.setStatus("Processing | " + (elapsed) + "s");
        }, 1000);
    }

    onStopProcessing() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = undefined;
        }
        if (this.startTime) {
            const elapsed = Math.round((Date.now() - this.startTime) / 1000);
            this.setStatus("Processed in " + (elapsed) + "s");
            this.startTime = 0;
        }
    }

    setStatus(status) {
        const statusBar = this.container.querySelector('.jscaffold-logview-status-bar');
        statusBar.innerHTML = status;
    }

}

function render({model, el}) {
    let container = document.createElement('div');
    const state = new LogViewState(container);
    container.innerHTML = `
    <div class="jscaffold-logview">
        <pre></pre>
        <div class="jscaffold-logview-copy-button">Copy</div>
    </div>
    <div class="jscaffold-logview-status-bar"></div>
    `;
    let pre = container.querySelector('pre');
    let copyButton = container.querySelector('.jscaffold-logview-copy-button');
    copyButton.addEventListener('click', () => {
        let range = document.createRange();
        range.selectNode(pre);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        document.execCommand('copy');
        window.getSelection().removeAllRanges();
    });

    model.on("change:value", () => {
        pre.textContent = model.get('value');
    });

    model.on("change:is_running", () => {
        const isRunning = model.get('is_running');
        if (isRunning) {
            state.onStartProcessing();
        } else {
            state.onStopProcessing();
        }
    });

    el.appendChild(container);
}


export default { render };
