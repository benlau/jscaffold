
function render({model, el}) {
    let container = document.createElement('div');
    container.classList.add('jscaffold-logview');
    container.innerHTML = `
        <pre></pre>
        <div class="jscaffold-logview-copy-button">Copy</div>
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

    el.appendChild(container);
}


export default { render };
