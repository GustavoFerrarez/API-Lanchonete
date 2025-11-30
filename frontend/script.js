// ========================================
// VARIÁVEIS GLOBAIS E CONFIGURAÇÃO DA API
// ========================================

const API_URL = "http://127.0.0.1:8000/v1"

// Elementos do DOM
const btnLogin = document.getElementById("btnLogin")
const modalLogin = document.getElementById("modalLogin")
const modalClose = document.getElementById("modalClose")
const loginForm = document.getElementById("loginForm")
const searchInput = document.getElementById("searchInput")
const cartBtn = document.getElementById("cartBtn")
const cartCount = document.getElementById("cartCount")

const userArea = document.getElementById("userArea")
const userLogged = document.getElementById("userLogged")
const userBtn = document.getElementById("userBtn")
const userDropdown = document.getElementById("userDropdown")
const userName = document.getElementById("userName")
const btnChangeAccount = document.getElementById("btnChangeAccount")
const btnLogout = document.getElementById("btnLogout")

const modalForgotPassword = document.getElementById("modalForgotPassword")
const modalForgotPasswordClose = document.getElementById("modalForgotPasswordClose")
const btnForgotPassword = document.getElementById("btnForgotPassword")
const btnBackToLoginFromForgot = document.getElementById("btnBackToLoginFromForgot")
const forgotPasswordForm = document.getElementById("forgotPasswordForm")

// Slider
const sliderPrev = document.getElementById("sliderPrev")
const sliderNext = document.getElementById("sliderNext")
let currentSlide = 0
let slides = []
let totalSlides = 0

// Modal do carrinho
const modalCart = document.getElementById("modalCart")
const modalCartClose = document.getElementById("modalCartClose")
const cartItemsList = document.getElementById("cartItemsList")
const cartEmpty = document.getElementById("cartEmpty")
const cartFooter = document.getElementById("cartFooter")
const cartTotal = document.getElementById("cartTotal")
const btnCheckout = document.getElementById("btnCheckout")

// Modal de formas de pagamento
const btnPaymentMethods = document.getElementById("btnPaymentMethods")
const modalPaymentMethods = document.getElementById("modalPaymentMethods")
const modalPaymentClose = document.getElementById("modalPaymentClose")

// Modal de mais informações
const btnMoreInfo = document.getElementById("btnMoreInfo")
const modalMoreInfo = document.getElementById("modalMoreInfo")
const modalInfoClose = document.getElementById("modalInfoClose")

// Modal de cadastro
const modalRegister = document.getElementById("modalRegister")
const modalRegisterClose = document.getElementById("modalRegisterClose")
const btnOpenRegister = document.getElementById("btnOpenRegister")
const btnBackToLogin = document.getElementById("btnBackToLogin")
const registerForm = document.getElementById("registerForm")

// Modal de taxa de entrega
const btnDeliveryFee = document.getElementById("btnDeliveryFee")
const modalDeliveryFee = document.getElementById("modalDeliveryFee")
const modalDeliveryClose = document.getElementById("modalDeliveryClose")

const modalCheckout = document.getElementById("modalCheckout")
const modalCheckoutClose = document.getElementById("modalCheckoutClose")
const checkoutForm = document.getElementById("checkoutForm")
const checkoutItemsList = document.getElementById("checkoutItemsList")
const checkoutTotal = document.getElementById("checkoutTotal")
const btnConfirmOrder = document.getElementById("btnConfirmOrder")

const modalSuccess = document.getElementById("modalSuccess")
const btnSuccessClose = document.getElementById("btnSuccessClose")
const successOrderNumber = document.getElementById("successOrderNumber")

// Seletor de Localização
const locationBtn = document.getElementById("locationBtn")
const locationDropdown = document.getElementById("locationDropdown")
const selectedCityText = document.getElementById("selectedCity")
const locationOptions = document.querySelectorAll(".location-option")
const googleMapIframe = document.getElementById("googleMap")
const addressCityElement = document.getElementById("addressCity")

// --- Variáveis de Estado da API ---
let usuarioId = null
let pedidoId = null
let produtoMap = {}
let usuarioNome = null // Armazena o nome do usuário logado

// ========================================
// CARGA DE PRODUTOS (CONECTADO)
// ========================================

async function loadProducts() {
  const menuContainer = document.getElementById("menu-container")
  if (!menuContainer) return

  menuContainer.innerHTML = '<h3 style="text-align:center">Carregando cardápio...</h3>'

  const categoriasNomes = {
    1: "Hambúrgueres Clássicos",
    2: "Hambúrgueres Gourmet",
    3: "Acompanhamentos",
  }

  try {
    const response = await fetch(`${API_URL}/produto/`)
    const produtos = await response.json()

    menuContainer.innerHTML = ""
    produtoMap = {}

    const produtosPorCategoria = {}

    produtos.forEach((produto) => {
      produtoMap[produto.id] = produto
      const catId = produto.categoria_id || 99

      if (!produtosPorCategoria[catId]) {
        produtosPorCategoria[catId] = []
      }
      produtosPorCategoria[catId].push(produto)
    })

    const categoriaIds = Object.keys(produtosPorCategoria).sort()

    categoriaIds.forEach((catId) => {
      const listaProdutos = produtosPorCategoria[catId]
      const nomeCategoria = categoriasNomes[catId] || "Outros Produtos"

      const categorySection = document.createElement("div")
      categorySection.className = "menu-category"

      categorySection.innerHTML = `
                <h2 class="category-title" data-collapsed="false">
                    <svg class="category-icon category-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                    ${nomeCategoria}
                </h2>
                <div class="products-grid category-${catId}"></div>
            `

      menuContainer.appendChild(categorySection)

      const grid = categorySection.querySelector(`.products-grid`)

      listaProdutos.forEach((produto) => {
        const card = document.createElement("div")
        card.className = "product-card"
        card.dataset.id = produto.id
        card.dataset.name = produto.nome
        card.dataset.price = produto.preco

        card.innerHTML = `
                    <h3 class="product-name">${produto.nome}</h3>
                    <p class="product-price">${formatPrice(produto.preco)}</p>
                    <p class="product-description">${produto.descricao || ""}</p>
                    <button class="btn-add-to-cart">Adicionar ao Carrinho</button>
                `
        grid.appendChild(card)
      })
    })

    addCartButtonListeners()
    addCategoryToggleListeners()
  } catch (err) {
    console.error(err)
    menuContainer.innerHTML = '<p style="text-align:center; color:red">Erro ao carregar cardápio. Verifique a API.</p>'
  }
}

function addCartButtonListeners() {
  const addToCartButtons = document.querySelectorAll(".btn-add-to-cart")
  addToCartButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.stopPropagation() 
      const productCard = this.closest(".product-card")
      const id = productCard.dataset.id
      const name = productCard.dataset.name
      addToCart(id, name)
    })
  })
}

function addCategoryToggleListeners() {
  const categoryTitles = document.querySelectorAll(".category-title")
  categoryTitles.forEach((title) => {
    title.addEventListener("click", function () {
      const isCollapsed = this.dataset.collapsed === "true"
      const productsGrid = this.nextElementSibling

      if (isCollapsed) {
        // Expandir
        this.dataset.collapsed = "false"
        this.classList.remove("collapsed")
        productsGrid.classList.remove("collapsed")
      } else {
        // Colapsar
        this.dataset.collapsed = "true"
        this.classList.add("collapsed")
        productsGrid.classList.add("collapsed")
      }
    })
  })
}

// ========================================
// MODAL DE LOGIN (CONECTADO)
// ========================================

function openModal() {
  modalLogin.classList.add("active")
  document.body.style.overflow = "hidden"
}

function closeModal() {
  modalLogin.classList.remove("active")
  document.body.style.overflow = "auto"
}

btnLogin.addEventListener("click", openModal)
modalClose.addEventListener("click", closeModal)
modalLogin.addEventListener("click", (e) => {
  if (e.target === modalLogin) closeModal()
})

function showLoggedState(nome) {
  btnLogin.style.display = "none"
  userLogged.style.display = "flex"
  userName.textContent = nome || "Usuário"
  usuarioNome = nome
}

function showLoggedOutState() {
  btnLogin.style.display = "block"
  userLogged.style.display = "none"
  userName.textContent = "Usuário"
  usuarioNome = null
  usuarioId = null
  pedidoId = null
}

userBtn.addEventListener("click", (e) => {
  e.stopPropagation()
  userDropdown.classList.toggle("active")
  userBtn.classList.toggle("active")
})

document.addEventListener("click", (e) => {
  if (!userBtn.contains(e.target) && !userDropdown.contains(e.target)) {
    userDropdown.classList.remove("active")
    userBtn.classList.remove("active")
  }
})

btnLogout.addEventListener("click", () => {
  if (confirm("Deseja realmente sair da conta?")) {
    showLoggedOutState()
    userDropdown.classList.remove("active")

    // Limpa o carrinho visual
    cartCount.textContent = "0"

    // Recarrega a página para resetar o estado
    const menuContainer = document.getElementById("menu-container")
    menuContainer.innerHTML = `
            <div style="text-align: center; padding: 50px; color: #666;">
                <h3>Faça login para visualizar o cardápio completo.</h3>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 48px; height: 48px; margin-top: 16px; opacity: 0.5;">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
            </div>
        `

    showNotification("Você saiu da conta")
  }
})

btnChangeAccount.addEventListener("click", () => {
  userDropdown.classList.remove("active")
  openModal()
})

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault()
  const email = document.getElementById("email").value
  const password = document.getElementById("password").value

  if (!email || !password) {
    showNotification("Por favor, preencha e-mail e senha.")
    return
}

  try {
    const userResponse = await fetch(`${API_URL}/usuario/`)
    if (!userResponse.ok) throw new Error("Falha ao buscar usuários.")
    const usuarios = await userResponse.json()

    // Buscando o usuário
    const usuarioEncontrado = usuarios.find(user => user.email === email);

    if (!usuarioEncontrado) {
      showNotification("E-mail não cadastrado.");
      return;
    }

    console.log("Senha digitada:", password);
    console.log("Senha no Banco:", usuarioEncontrado.senha);

    const senhaDoBanco = usuarioEncontrado.senha || "";

    if (usuarios.length === 0) {
      showNotification("Nenhum usuário cadastrado. Crie um usuário primeiro na tela de cadastro.")
      return
    }
    usuarioId = usuarioEncontrado.id
    const nomeUsuario = usuarioEncontrado.nome || "Usuário"

    const pedidoResponse = await fetch(`${API_URL}/pedido/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usuario_id: usuarioId, observacoes: "Novo pedido" }),
    })
    if (!pedidoResponse.ok) throw new Error("Falha ao criar novo pedido.")

    const novoPedido = await pedidoResponse.json()
    pedidoId = novoPedido.id

    showLoggedState(nomeUsuario)

    showNotification(`Bem-vindo, ${nomeUsuario}!`)
    closeModal()

    await loadProducts()
    await updateCartCount()
  } catch (err) {
    console.error(err)
    showNotification(err.message)
  }
})


// ========================================

function openForgotPasswordModal() {
  modalLogin.classList.remove("active")
  modalForgotPassword.classList.add("active")
  document.body.style.overflow = "hidden"
}

function closeForgotPasswordModal() {
  modalForgotPassword.classList.remove("active")
  document.body.style.overflow = "auto"
}

function backToLoginFromForgot() {
  modalForgotPassword.classList.remove("active")
  modalLogin.classList.add("active")
}

btnForgotPassword.addEventListener("click", (e) => {
  e.preventDefault()
  openForgotPasswordModal()
})

btnBackToLoginFromForgot.addEventListener("click", (e) => {
  e.preventDefault()
  backToLoginFromForgot()
})

modalForgotPasswordClose.addEventListener("click", closeForgotPasswordModal)

modalForgotPassword.addEventListener("click", (e) => {
  if (e.target === modalForgotPassword) closeForgotPasswordModal()
})

forgotPasswordForm.addEventListener("submit", async (e) => {
  e.preventDefault()
  const email = document.getElementById("forgotEmail").value

  if (!email) {
    showNotification("Por favor, digite seu e-mail.")
    return
  }

  // Simulação de envio de e-mail de recuperação
  try {
    await new Promise((resolve) => setTimeout(resolve, 1000))

    showNotification(
      `Link de recuperação enviado para: ${email}\n\n(Esta é uma simulação.)`,
    )
    closeForgotPasswordModal()
    forgotPasswordForm.reset()
    openModal() // Volta para o login
  } catch (err) {
    console.error(err)
    showNotification("Erro ao enviar e-mail de recuperação. Tente novamente.")
  }
})

// ========================================
// MODAL DE CADASTRO (CONECTADO)
// ========================================

function openRegisterModal() {
  modalLogin.classList.remove("active")
  modalRegister.classList.add("active")
  document.body.style.overflow = "hidden"
}

function closeRegisterModal() {
  modalRegister.classList.remove("active")
  document.body.style.overflow = "auto"
}

function backToLogin() {
  modalRegister.classList.remove("active")
  modalLogin.classList.add("active")
}

btnOpenRegister.addEventListener("click", (e) => {
  e.preventDefault()
  openRegisterModal()
})
btnBackToLogin.addEventListener("click", (e) => {
  e.preventDefault()
  backToLogin()
})
modalRegisterClose.addEventListener("click", closeRegisterModal)

registerForm.addEventListener("submit", async (e) => {
  e.preventDefault()

  const nome = document.getElementById("registerName").value
  const email = document.getElementById("registerEmail").value
  const phone = document.getElementById("registerPhone").value
  const senha = document.getElementById("registerPassword").value
  const passwordConfirm = document.getElementById("registerPasswordConfirm").value

  if (senha !== passwordConfirm) {
    showNotification("As senhas não coincidem!")
    return
  }

  try {
    const response = await fetch(`${API_URL}/usuario/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nome, email, senha, tipo_usuario: "cliente" }),
    })

    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.detail || "Falha ao criar usuário.")
    }

    const novoUsuario = await response.json()
    showNotification(`Usuário ${novoUsuario.nome} (ID: ${novoUsuario.id}) criado! Agora faça o login.`)
    closeRegisterModal()
    registerForm.reset()
  } catch (err) {
    console.error(err)
    showNotification(err.message)
  }
})

// ========================================
// CARRINHO DE COMPRAS (CONECTADO)
// ========================================

function openCartModal() {
  modalCart.classList.add("active")
  document.body.style.overflow = "hidden"
  updateCartDisplay()
}

function closeCartModal() {
  modalCart.classList.remove("active")
  document.body.style.overflow = "auto"
}

cartBtn.addEventListener("click", openCartModal)
modalCartClose.addEventListener("click", closeCartModal)

async function addToCart(produtoId, nome) {
  if (!pedidoId) {
    showNotification("Você precisa fazer o login primeiro!")
    openModal()
    return
  }

  const payload = {
    produto_id: Number.parseInt(produtoId),
    quantidade: 1,
    pedido_id: pedidoId,
  }

  try {
    const response = await fetch(`${API_URL}/item_pedido/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.detail || "Erro ao adicionar item.")
    }

    showNotification(`✓ ${nome} adicionado`)
    await updateCartCount()
  } catch (err) {
    console.error(err)
    showNotification(err.message)
  }
}

let itemToDeleteId = null;

// Elementos do Modal de Confirmação
const modalConfirmDelete = document.getElementById('modalConfirmDelete');
const btnCancelDelete = document.getElementById('btnCancelDelete');
const btnConfirmDelete = document.getElementById('btnConfirmDelete');

// 1. Função chamada ao clicar na lixeira (SÓ ABRE O MODAL)
function removeFromCart(itemId) {
    itemToDeleteId = itemId; 
    modalConfirmDelete.classList.add('active'); 
}

// 2. Ação do botão "Cancelar"
btnCancelDelete.addEventListener('click', () => {
    modalConfirmDelete.classList.remove('active');
    itemToDeleteId = null;
});

// 3. Ação do botão "Sim, remover" (AQUI DELETA DE VERDADE)
btnConfirmDelete.addEventListener('click', async () => {
    if (!itemToDeleteId) return;

    try {
        // Fecha o modal
        modalConfirmDelete.classList.remove('active');

        // Faz a chamada para a API (código original)
        const response = await fetch(`${API_URL}/item_pedido/${itemToDeleteId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Falha ao remover item.');

        // Atualiza a tela
        await updateCartDisplay();
        await updateCartCount();
        
        showNotification("Item removido com sucesso");

    } catch (err) {
        console.error(err);
        showNotification(err.message);
    } finally {
        itemToDeleteId = null; 
    }
});

// Fecha se clicar fora do modal
modalConfirmDelete.addEventListener('click', (e) => {
    if (e.target === modalConfirmDelete) {
        modalConfirmDelete.classList.remove('active');
        itemToDeleteId = null;
    }
});

async function updateQuantity(itemId, newQuantity) {
  if (newQuantity <= 0) {
    removeFromCart(itemId)
    return
  }
  try {
    const response = await fetch(`${API_URL}/item_pedido/${itemId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ quantidade: newQuantity }),
    })
    if (!response.ok) throw new Error("Falha ao atualizar quantidade.")

    await updateCartDisplay()
    await updateCartCount()
  } catch (err) {
    console.error(err)
    showNotification(err.message)
  }
}

async function updateCartCount() {
  if (!pedidoId) {
    cartCount.textContent = "0"
    return
  }

  try {
    const response = await fetch(`${API_URL}/item_pedido/pedido/${pedidoId}`)
    const itens = await response.json()
    const totalItems = itens.reduce((sum, item) => sum + item.quantidade, 0)
    cartCount.textContent = totalItems
  } catch (err) {
    cartCount.textContent = "0"
  }
}

async function updateCartDisplay() {
    if (!pedidoId) return;

    
    cartItemsList.style.opacity = '0.5';
    cartItemsList.style.pointerEvents = 'none'; 

    try {
        const response = await fetch(`${API_URL}/item_pedido/pedido/${pedidoId}`);
        if (!response.ok) throw new Error('Falha ao buscar carrinho.');
        const itensSemOrdem = await response.json();

        const itens = itensSemOrdem.sort((a, b) => a.id - b.id);

        cartItemsList.innerHTML = '';
        
        // Remove a transparência (volta ao normal)
        cartItemsList.style.opacity = '1';
        cartItemsList.style.pointerEvents = 'auto';

        if (itens.length === 0) {
            cartEmpty.style.display = 'block';
            cartFooter.style.display = 'none';
            cartTotal.textContent = formatPrice(0);
            return;
        }

        cartEmpty.style.display = 'none';
        cartFooter.style.display = 'block';

        let total = 0;

        itens.forEach(item => {
            const produto = produtoMap[item.produto_id];
            const nome = produto ? produto.nome : `Produto ID: ${item.produto_id}`;
            const itemTotal = item.preco_unitario * item.quantidade;
            total += itemTotal;

            const cartItem = document.createElement('div');
            cartItem.className = 'cart-item';
            
            cartItem.style.animation = 'fadeIn 0.3s ease'; 
            
            cartItem.innerHTML = `
                <div class="cart-item-info">
                    <div class="cart-item-name">${nome}</div>
                    <div class="cart-item-price">${formatPrice(item.preco_unitario)}</div>
                </div>
                <div class="cart-item-quantity">
                    <button class="quantity-btn" onclick="updateQuantity(${item.id}, ${item.quantidade - 1})">-</button>
                    <span class="quantity-value">${item.quantidade}</span>
                    <button class="quantity-btn" onclick="updateQuantity(${item.id}, ${item.quantidade + 1})">+</button>
                </div>
                <button class="cart-item-remove" onclick="removeFromCart(${item.id})">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                </button>
            `;
            cartItemsList.appendChild(cartItem);
        });

        cartTotal.textContent = formatPrice(total);

    } catch (err) {
        console.error(err);
        cartItemsList.style.opacity = '1'; // Garante que volta ao normal se der erro
        cartItemsList.innerHTML = '<p>Erro ao carregar carrinho.</p>';
    }
}

btnCheckout.addEventListener("click", async () => {
  if (!pedidoId || !usuarioId) return

  // Abre o modal de checkout ao invés de usar confirm()
  openCheckoutModal()
})

// ========================================
// MODAL DE CHECKOUT
// ========================================

function openCheckoutModal() {
  modalCart.classList.remove("active")
  modalCheckout.classList.add("active")
  document.body.style.overflow = "hidden"
  updateCheckoutDisplay()
}

function closeCheckoutModal() {
  modalCheckout.classList.remove("active")
  document.body.style.overflow = "auto"
}

modalCheckoutClose.addEventListener("click", closeCheckoutModal)
modalCheckout.addEventListener("click", (e) => {
  if (e.target === modalCheckout) closeCheckoutModal()
})

async function updateCheckoutDisplay() {
  if (!pedidoId) return

  checkoutItemsList.innerHTML = "Carregando..."

  try {
    const response = await fetch(`${API_URL}/item_pedido/pedido/${pedidoId}`)
    if (!response.ok) throw new Error("Falha ao buscar itens.")
    const itens = await response.json()

    checkoutItemsList.innerHTML = ""
    let total = 0

    itens.forEach((item) => {
      const produto = produtoMap[item.produto_id]
      const nome = produto ? produto.nome : `Produto ID: ${item.produto_id}`
      const itemTotal = item.preco_unitario * item.quantidade
      total += itemTotal

      const checkoutItem = document.createElement("div")
      checkoutItem.className = "checkout-item"
      checkoutItem.innerHTML = `
        <span class="checkout-item-qty">${item.quantidade}x</span>
        <span class="checkout-item-name">${nome}</span>
        <span class="checkout-item-price">${formatPrice(itemTotal)}</span>
      `
      checkoutItemsList.appendChild(checkoutItem)
    })

    checkoutTotal.textContent = formatPrice(total)
  } catch (err) {
    console.error(err)
    checkoutItemsList.innerHTML = "<p>Erro ao carregar itens.</p>"
  }
}

btnConfirmOrder.addEventListener("click", async () => {
  // Validar campos obrigatórios
  const street = document.getElementById("checkoutStreet").value.trim()
  const number = document.getElementById("checkoutNumber").value.trim()
  const neighborhood = document.getElementById("checkoutNeighborhood").value.trim()
  const cep = document.getElementById("checkoutCep").value.trim()

  if (!street || !number || !neighborhood || !cep) {
    showNotification("Por favor, preencha todos os campos obrigatórios do endereço.")
    return
  }

  try {
    // Finaliza o pedido atual
    const response = await fetch(`${API_URL}/pedido/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usuario_id: usuarioId, observacoes: "Novo pedido" }),
    })
    if (!response.ok) throw new Error("Falha ao criar novo pedido.")

    const novoPedido = await response.json()
    const pedidoAnterior = pedidoId
    pedidoId = novoPedido.id

    // Fecha modal de checkout e abre modal de sucesso
    closeCheckoutModal()
    openSuccessModal(pedidoAnterior)

    // Limpa o formulário
    checkoutForm.reset()

    await updateCartDisplay()
    await updateCartCount()
  } catch (err) {
    console.error(err)
    showNotification("Erro ao finalizar pedido. Tente novamente.")
  }
})

// ========================================
// MODAL DE SUCESSO
// ========================================

function openSuccessModal(orderNumber) {
  successOrderNumber.textContent = orderNumber || "0000"
  modalSuccess.classList.add("active")
  document.body.style.overflow = "hidden"
}

function closeSuccessModal() {
  modalSuccess.classList.remove("active")
  document.body.style.overflow = "auto"
}

btnSuccessClose.addEventListener("click", closeSuccessModal)
modalSuccess.addEventListener("click", (e) => {
  if (e.target === modalSuccess) closeSuccessModal()
})

// ========================================
// SLIDER, BUSCA, MODAIS (LÓGICA DA UI)
// ========================================

function initSlider() {
  slides = document.querySelectorAll(".hero-slide")
  totalSlides = slides.length
  if (totalSlides > 0) showSlide(0)
}
function showSlide(index) {
  if (totalSlides === 0) return
  slides.forEach((slide) => slide.classList.remove("active"))
  if (index >= totalSlides) currentSlide = 0
  else if (index < 0) currentSlide = totalSlides - 1
  else currentSlide = index
  slides[currentSlide].classList.add("active")
}
function nextSlide() {
  showSlide(currentSlide + 1)
}
function prevSlide() {
  showSlide(currentSlide - 1)
}
if (sliderNext) sliderNext.addEventListener("click", nextSlide)
if (sliderPrev) sliderPrev.addEventListener("click", prevSlide)
setInterval(nextSlide, 5000)

searchInput.addEventListener("input", (e) => {
  const searchTerm = e.target.value.toLowerCase()
  const productCards = document.querySelectorAll(".product-card")

  productCards.forEach((card) => {
    const name = card.querySelector(".product-name").textContent.toLowerCase()
    const description = card.querySelector(".product-description").textContent.toLowerCase()
    if (name.includes(searchTerm) || description.includes(searchTerm)) {
      card.style.display = "block"
    } else {
      card.style.display = "none"
    }
  })
})

function openPaymentModal() {
  modalPaymentMethods.classList.add("active")
  document.body.style.overflow = "hidden"
}
function closePaymentModal() {
  modalPaymentMethods.classList.remove("active")
  document.body.style.overflow = "auto"
}
btnPaymentMethods.addEventListener("click", openPaymentModal)
modalPaymentClose.addEventListener("click", closePaymentModal)
modalPaymentMethods.addEventListener("click", (e) => {
  if (e.target === modalPaymentMethods) closePaymentModal()
})

function openInfoModal() {
  modalMoreInfo.classList.add("active")
  document.body.style.overflow = "hidden"
}
function closeInfoModal() {
  modalMoreInfo.classList.remove("active")
  document.body.style.overflow = "auto"
}
btnMoreInfo.addEventListener("click", openInfoModal)
modalInfoClose.addEventListener("click", closeInfoModal)
modalMoreInfo.addEventListener("click", (e) => {
  if (e.target === modalMoreInfo) closeInfoModal()
})

function openDeliveryFeeModal() {
  modalDeliveryFee.classList.add("active")
  document.body.style.overflow = "hidden"
}
function closeDeliveryFeeModal() {
  modalDeliveryFee.classList.remove("active")
  document.body.style.overflow = "auto"
}
btnDeliveryFee.addEventListener("click", openDeliveryFeeModal)
modalDeliveryClose.addEventListener("click", closeDeliveryFeeModal)
modalDeliveryFee.addEventListener("click", (e) => {
  if (e.target === modalDeliveryFee) closeDeliveryFeeModal()
})

const citiesData = {
  "São Sebastião do Paraíso": { mapUrl: "..." },
  Itamogi: { mapUrl: "..." },
  "São Paulo": { mapUrl: "..." },
}
function toggleLocationDropdown() {
  locationDropdown.classList.toggle("active")
  locationBtn.classList.toggle("active")
}
function closeLocationDropdown() {
  locationDropdown.classList.remove("active")
  locationBtn.classList.remove("active")
}
function updateSelectedCity(city, state) {
  selectedCityText.textContent = `${city} - ${state}`
  if (addressCityElement) addressCityElement.textContent = `${city} - ${state}`
  if (googleMapIframe && citiesData[city]) googleMapIframe.src = citiesData[city].mapUrl
  locationOptions.forEach((option) => {
    option.classList.remove("selected")
    if (option.dataset.city === city) option.classList.add("selected")
  })
  closeLocationDropdown()
}
locationBtn.addEventListener("click", (e) => {
  e.stopPropagation()
  toggleLocationDropdown()
})
locationOptions.forEach((option) => {
  option.addEventListener("click", (e) => {
    e.stopPropagation()
    updateSelectedCity(option.dataset.city, option.dataset.state)
  })
})
document.addEventListener("click", (e) => {
  if (!locationBtn.contains(e.target) && !locationDropdown.contains(e.target)) closeLocationDropdown()
})

// ========================================
// INICIALIZAÇÃO E UTILITÁRIOS
// ========================================

document.addEventListener("DOMContentLoaded", () => {
  console.log("BurguerHouse (CONECTADA) carregada!")
  initSlider()
})

function formatPrice(value) {
  return new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(value)
}

function showNotification(message) {
  const notification = document.createElement("div")
  notification.textContent = message
  notification.style.cssText = `
        position: fixed; bottom: 24px; right: 24px; background-color: var(--primary-color);
        color: white; padding: 16px 24px; border-radius: 8px;
        box-shadow: var(--shadow-lg); z-index: 3000; animation: slideIn 0.3s ease;`
  document.body.appendChild(notification)
  setTimeout(() => {
    notification.style.animation = "slideOut 0.3s ease"
    setTimeout(() => {
      document.body.removeChild(notification)
    }, 300)
  }, 3000)
}

const style = document.createElement("style")
style.textContent = `
    @keyframes slideIn { from { transform: translateX(400px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
    @keyframes slideOut { from { transform: translateX(0); opacity: 1; } to { transform: translateX(400px); opacity: 0; } }
`
document.head.appendChild(style)
