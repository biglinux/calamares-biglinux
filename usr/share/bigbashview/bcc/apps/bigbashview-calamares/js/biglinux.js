const fileInput = document.getElementById("fileInput");
const textArea = document.getElementById("install_packages");

fileInput.addEventListener("change", function() {
  const file = fileInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      textArea.value = e.target.result;
    };
    reader.readAsText(file);
  } else {
    textArea.value = ""; // Limpa o <textarea> se nenhum arquivo for selecionado
  }
});

const fileInput2 = document.getElementById("fileInput2");
const textArea2 = document.getElementById("remove_packages");

fileInput2.addEventListener("change", function() {
  const file = fileInput2.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      textArea2.value = e.target.result;
    };
    reader.readAsText(file);
  } else {
    textArea2.value = ""; // Limpa o <textarea> se nenhum arquivo for selecionado
  }
});
