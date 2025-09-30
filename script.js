// Configurações da API
const API_BASE_URL = '/api';

// Estado da aplicação
let currentPage = 1;
let currentFilter = '';

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupEventListeners();
    loadCobrancas();
}

function setupEventListeners() {
    // Navegação entre tabs
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });

    // Formulário de criação de cobrança
    document.getElementById('form-cobranca').addEventListener('submit', handleCreateCobranca);

    // Filtros e refresh
    document.getElementById('filter-status').addEventListener('change', function() {
        currentFilter = this.value;
        currentPage = 1;
        loadCobrancas();
    });

    document.getElementById('btn-refresh').addEventListener('click', function() {
        loadCobrancas();
    });

    // Modal
    document.querySelector('.modal-close').addEventListener('click', closeModal);
    document.getElementById('modal-detalhes').addEventListener('click', function(e) {
        if (e.target === this) {
            closeModal();
        }
    });

    // Máscaras para inputs
    setupInputMasks();
}

function setupInputMasks() {
    // Máscara para telefone
    const telefoneInput = document.getElementById('cliente_telefone');
    telefoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length <= 11) {
            value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
            if (value.length < 14) {
                value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
            }
        }
        e.target.value = value;
    });

    // Máscara para CPF/CNPJ
    const documentoInput = document.getElementById('cliente_documento');
    documentoInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length <= 11) {
            // CPF
            value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
        } else {
            // CNPJ
            value = value.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
        }
        e.target.value = value;
    });
}

function switchTab(tabName) {
    // Atualizar botões de navegação
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Mostrar/esconder conteúdo
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`tab-${tabName}`).classList.add('active');

    // Carregar dados se necessário
    if (tabName === 'listar') {
        loadCobrancas();
    }
}

async function handleCreateCobranca(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    // Validar dados
    if (!data.cliente_nome || !data.cliente_email || !data.titulo || !data.valor) {
        showToast('Preencha todos os campos obrigatórios', 'error');
        return;
    }

    // Converter valor para número
    data.valor = parseFloat(data.valor);

    try {
        showLoading(true);
        
        const response = await fetch(`${API_BASE_URL}/cobrancas`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showToast('Cobrança criada com sucesso!', 'success');
            e.target.reset();
            
            // Mostrar detalhes da cobrança criada
            showCobrancaDetails(result);
        } else {
            showToast(`Erro: ${result.error}`, 'error');
        }
    } catch (error) {
        showToast(`Erro de conexão: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

async function loadCobrancas(page = 1) {
    try {
        showLoading(true);
        
        let url = `${API_BASE_URL}/cobrancas?page=${page}&per_page=10`;
        if (currentFilter) {
            url += `&status=${currentFilter}`;
        }

        const response = await fetch(url);
        const result = await response.json();

        if (result.success) {
            displayCobrancas(result.cobrancas);
            displayPagination(result.current_page, result.pages, result.total);
        } else {
            showToast(`Erro ao carregar cobranças: ${result.error}`, 'error');
        }
    } catch (error) {
        showToast(`Erro de conexão: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

function displayCobrancas(cobrancas) {
    const container = document.getElementById('cobrancas-container');
    
    if (cobrancas.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: #6c757d;">
                <i class="fas fa-inbox fa-3x" style="margin-bottom: 1rem; opacity: 0.5;"></i>
                <p>Nenhuma cobrança encontrada</p>
            </div>
        `;
        return;
    }

    container.innerHTML = cobrancas.map(cobranca => `
        <div class="cobranca-item" onclick="showCobrancaModal(${cobranca.id})">
            <div class="cobranca-header">
                <div>
                    <div class="cobranca-title">${cobranca.titulo}</div>
                    <div class="cobranca-reference">Ref: ${cobranca.external_reference}</div>
                </div>
                <div class="cobranca-valor">R$ ${cobranca.valor.toFixed(2)}</div>
            </div>
            
            <div class="cobranca-info">
                <div class="cobranca-info-item">
                    <div class="cobranca-info-label">Cliente</div>
                    <div class="cobranca-info-value">${cobranca.cliente_nome}</div>
                </div>
                <div class="cobranca-info-item">
                    <div class="cobranca-info-label">Email</div>
                    <div class="cobranca-info-value">${cobranca.cliente_email}</div>
                </div>
                <div class="cobranca-info-item">
                    <div class="cobranca-info-label">Status</div>
                    <div class="cobranca-info-value">
                        <span class="status-badge status-${cobranca.status}">${getStatusText(cobranca.status)}</span>
                    </div>
                </div>
                <div class="cobranca-info-item">
                    <div class="cobranca-info-label">Data</div>
                    <div class="cobranca-info-value">${formatDate(cobranca.data_criacao)}</div>
                </div>
            </div>
            
            <div class="cobranca-actions">
                ${cobranca.payment_url ? `<a href="${cobranca.payment_url}" target="_blank" class="btn btn-success btn-sm">
                    <i class="fas fa-external-link-alt"></i> Pagar
                </a>` : ''}
                <button onclick="event.stopPropagation(); reenviarEmail(${cobranca.id})" class="btn btn-warning btn-sm">
                    <i class="fas fa-envelope"></i> Reenviar Email
                </button>
                <button onclick="event.stopPropagation(); showCobrancaModal(${cobranca.id})" class="btn btn-secondary btn-sm">
                    <i class="fas fa-eye"></i> Detalhes
                </button>
            </div>
        </div>
    `).join('');
}

function displayPagination(currentPage, totalPages, totalItems) {
    const container = document.getElementById('pagination');
    
    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }

    let pagination = `
        <button onclick="loadCobrancas(1)" ${currentPage === 1 ? 'disabled' : ''}>
            <i class="fas fa-angle-double-left"></i>
        </button>
        <button onclick="loadCobrancas(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
            <i class="fas fa-angle-left"></i>
        </button>
    `;

    // Páginas numeradas
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);

    for (let i = startPage; i <= endPage; i++) {
        pagination += `
            <button onclick="loadCobrancas(${i})" ${i === currentPage ? 'class="active"' : ''}>
                ${i}
            </button>
        `;
    }

    pagination += `
        <button onclick="loadCobrancas(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
            <i class="fas fa-angle-right"></i>
        </button>
        <button onclick="loadCobrancas(${totalPages})" ${currentPage === totalPages ? 'disabled' : ''}>
            <i class="fas fa-angle-double-right"></i>
        </button>
    `;

    container.innerHTML = pagination;
}

async function showCobrancaModal(cobrancaId) {
    try {
        const response = await fetch(`${API_BASE_URL}/cobrancas/${cobrancaId}`);
        const result = await response.json();

        if (result.success) {
            const cobranca = result.cobranca;
            
            document.getElementById('modal-body').innerHTML = `
                <div class="cobranca-details">
                    <div class="detail-section">
                        <h4><i class="fas fa-info-circle"></i> Informações Gerais</h4>
                        <div class="detail-grid">
                            <div class="detail-item">
                                <strong>ID:</strong> ${cobranca.id}
                            </div>
                            <div class="detail-item">
                                <strong>Referência:</strong> ${cobranca.external_reference}
                            </div>
                            <div class="detail-item">
                                <strong>Mercado Pago ID:</strong> ${cobranca.mercadopago_id || 'N/A'}
                            </div>
                            <div class="detail-item">
                                <strong>Status:</strong> 
                                <span class="status-badge status-${cobranca.status}">${getStatusText(cobranca.status)}</span>
                            </div>
                        </div>
                    </div>

                    <div class="detail-section">
                        <h4><i class="fas fa-user"></i> Cliente</h4>
                        <div class="detail-grid">
                            <div class="detail-item">
                                <strong>Nome:</strong> ${cobranca.cliente_nome}
                            </div>
                            <div class="detail-item">
                                <strong>Email:</strong> ${cobranca.cliente_email}
                            </div>
                            <div class="detail-item">
                                <strong>Telefone:</strong> ${cobranca.cliente_telefone || 'N/A'}
                            </div>
                            <div class="detail-item">
                                <strong>Documento:</strong> ${cobranca.cliente_documento || 'N/A'}
                            </div>
                        </div>
                    </div>

                    <div class="detail-section">
                        <h4><i class="fas fa-shopping-cart"></i> Cobrança</h4>
                        <div class="detail-grid">
                            <div class="detail-item">
                                <strong>Título:</strong> ${cobranca.titulo}
                            </div>
                            <div class="detail-item">
                                <strong>Descrição:</strong> ${cobranca.descricao || 'N/A'}
                            </div>
                            <div class="detail-item">
                                <strong>Valor:</strong> <span style="color: #28a745; font-weight: bold;">R$ ${cobranca.valor.toFixed(2)}</span>
                            </div>
                        </div>
                    </div>

                    <div class="detail-section">
                        <h4><i class="fas fa-calendar"></i> Datas</h4>
                        <div class="detail-grid">
                            <div class="detail-item">
                                <strong>Criação:</strong> ${formatDateTime(cobranca.data_criacao)}
                            </div>
                            <div class="detail-item">
                                <strong>Atualização:</strong> ${formatDateTime(cobranca.data_atualizacao)}
                            </div>
                            <div class="detail-item">
                                <strong>Pagamento:</strong> ${cobranca.data_pagamento ? formatDateTime(cobranca.data_pagamento) : 'N/A'}
                            </div>
                        </div>
                    </div>

                    ${cobranca.payment_url ? `
                        <div class="detail-section">
                            <h4><i class="fas fa-link"></i> Link de Pagamento</h4>
                            <div style="margin-top: 1rem;">
                                <a href="${cobranca.payment_url}" target="_blank" class="btn btn-success">
                                    <i class="fas fa-external-link-alt"></i> Abrir Link de Pagamento
                                </a>
                            </div>
                        </div>
                    ` : ''}
                </div>

                <style>
                    .cobranca-details { }
                    .detail-section { margin-bottom: 2rem; }
                    .detail-section h4 { 
                        color: #667eea; 
                        margin-bottom: 1rem; 
                        display: flex; 
                        align-items: center; 
                        gap: 0.5rem; 
                    }
                    .detail-grid { 
                        display: grid; 
                        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                        gap: 1rem; 
                    }
                    .detail-item { 
                        padding: 0.75rem; 
                        background: #f8f9fa; 
                        border-radius: 5px; 
                    }
                </style>
            `;

            document.getElementById('modal-detalhes').style.display = 'block';
        } else {
            showToast(`Erro ao carregar detalhes: ${result.error}`, 'error');
        }
    } catch (error) {
        showToast(`Erro de conexão: ${error.message}`, 'error');
    }
}

function showCobrancaDetails(cobrancaData) {
    const details = `
        <div style="text-align: center; padding: 1rem;">
            <h3 style="color: #28a745; margin-bottom: 1rem;">
                <i class="fas fa-check-circle"></i> Cobrança Criada!
            </h3>
            <p><strong>ID:</strong> ${cobrancaData.cobranca_id}</p>
            <p><strong>Referência:</strong> ${cobrancaData.external_reference}</p>
            <p><strong>Email enviado:</strong> ${cobrancaData.email_enviado ? 'Sim' : 'Não'}</p>
            ${cobrancaData.payment_url ? `
                <div style="margin-top: 1rem;">
                    <a href="${cobrancaData.payment_url}" target="_blank" class="btn btn-success">
                        <i class="fas fa-external-link-alt"></i> Abrir Link de Pagamento
                    </a>
                </div>
            ` : ''}
        </div>
    `;
    
    document.getElementById('modal-body').innerHTML = details;
    document.getElementById('modal-detalhes').style.display = 'block';
}

async function reenviarEmail(cobrancaId) {
    try {
        const response = await fetch(`${API_BASE_URL}/cobrancas/${cobrancaId}/reenviar-email`, {
            method: 'POST'
        });

        const result = await response.json();

        if (result.success) {
            showToast('Email reenviado com sucesso!', 'success');
        } else {
            showToast(`Erro ao reenviar email: ${result.error}`, 'error');
        }
    } catch (error) {
        showToast(`Erro de conexão: ${error.message}`, 'error');
    }
}

function closeModal() {
    document.getElementById('modal-detalhes').style.display = 'none';
}

function showLoading(show) {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = show ? 'block' : 'none';
    }
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const icon = document.querySelector('.toast-icon');
    const messageEl = document.querySelector('.toast-message');

    // Definir ícone baseado no tipo
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };

    icon.className = `toast-icon ${icons[type] || icons.info}`;
    messageEl.textContent = message;
    toast.className = `toast ${type}`;

    // Mostrar toast
    toast.classList.add('show');

    // Esconder após 5 segundos
    setTimeout(() => {
        toast.classList.remove('show');
    }, 5000);
}

function getStatusText(status) {
    const statusMap = {
        pending: 'Pendente',
        approved: 'Aprovado',
        rejected: 'Rejeitado',
        cancelled: 'Cancelado',
        in_process: 'Processando'
    };
    return statusMap[status] || status;
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

function formatDateTime(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR');
}
