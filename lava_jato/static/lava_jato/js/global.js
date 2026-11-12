// LavaControl - JavaScript global
document.addEventListener("DOMContentLoaded", () => {
  // Mostrar/ocultar senha
  const password = document.querySelector("#password");
  const passwordToggle = document.querySelector(".password-toggle");

  if (password && passwordToggle) {
    passwordToggle.addEventListener("click", () => {
      const isPassword = password.type === "password";
      password.type = isPassword ? "text" : "password";
      passwordToggle.textContent = isPassword ? "◉" : "◌";
    });
  }



  // Cadastro de lavagem
  const washForm = document.querySelector("#wash-form");
  if (washForm) {
    washForm.addEventListener("submit", (event) => {
    });
  }

  // Cancelar cadastro
  document.querySelectorAll("[data-cancel]").forEach((button) => {
    button.addEventListener("click", () => window.history.back());
  });

  // Ações historico: editar e excluir 

});

// LavaControl - Sistema de notificações

// LavaControl - Sistema de notificações Toast

document.addEventListener("DOMContentLoaded", function () {

    const toasts = document.querySelectorAll(".toast");

    toasts.forEach(function (toast) {

        let removido = false;

        function fecharToast() {
            if (removido) return;

            removido = true;

            toast.classList.add("removing");

            setTimeout(function () {
                toast.remove();
            }, 300);
        }

        // Fechar pelo botão X
        const botaoFechar = toast.querySelector(".toast-close");

        if (botaoFechar) {
            botaoFechar.addEventListener("click", fecharToast);
        }

        // Remover automaticamente após 4 segundos
        setTimeout(fecharToast, 4000);

    });

});

//Modal de exclusão de lavagem

let formularioExclusao = null;

function abrirModalExclusao(botao) {
    formularioExclusao = botao.closest("form");

    document
        .getElementById("modal-exclusao")
        .classList.add("active");
}

function fecharModalExclusao() {
    document
        .getElementById("modal-exclusao")
        .classList.remove("active");

    formularioExclusao = null;
}

function confirmarExclusao() {
    if (formularioExclusao) {
        formularioExclusao.submit();
    }
}

// Fechar clicando fora do modal
document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("modal-exclusao");

    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            fecharModalExclusao();
        }
    });
});

