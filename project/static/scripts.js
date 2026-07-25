const mdeditor = document.getElementById("id_content");
if (mdeditor) {
	document.querySelectorAll(".toolbar button").forEach(btn => {
		btn.addEventListener("click", () => {
			const before = btn.dataset.before ? btn.dataset.before : "";
			const after = btn.dataset.after ? btn.dataset.after : "";
			const start = mdeditor.selectionStart;
			const end = mdeditor.selectionEnd;
			const selected = mdeditor.value.substring(start, end);
			mdeditor.setRangeText(before + selected + after, start, end, "select");
			mdeditor.focus();
		});
	});
}
