// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Para chamadas API
import './App.css';
import EEGPlot from './components/EEGPlot'; // Importar o novo componente

// Configuração base da API (ajuste conforme necessário)
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'; // Use variável de ambiente ou fallback

function App() {
    const [message, setMessage] = useState('');
    const [edfFiles, setEdfFiles] = useState([]); // Lista de arquivos EDF do usuário
    const [selectedEdfId, setSelectedEdfId] = useState(null);
    const [processingStatus, setProcessingStatus] = useState({}); // { fileId: 'status' }
    const [authToken, setAuthToken] = useState(localStorage.getItem('authToken')); // Simulação de auth

    // Simulação de login e obtenção de token
    const handleLogin = async (email, password) => {
        try {
            // Em uma app real, esta seria uma chamada POST para /auth/login
            // const response = await axios.post(`${API_BASE_URL}/auth/login`, { email, password });
            // const token = response.data.access_token;
            
            // Simulação:
            const token = "fake_jwt_token_for_testing"; 
            localStorage.setItem('authToken', token);
            setAuthToken(token);
            console.log("Login simulado com sucesso. Token:", token);
            fetchEdfFiles(token); // Busca arquivos após login
        } catch (error) {
            console.error("Erro no login (simulado):", error);
            alert("Falha no login (simulado). Verifique o console.");
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('authToken');
        setAuthToken(null);
        setEdfFiles([]);
        setSelectedEdfId(null);
        console.log("Logout simulado.");
    };

    // Buscar a lista de arquivos EDF do backend
    const fetchEdfFiles = async (token) => {
        if (!token) return;
        try {
            // const response = await axios.get(`${API_BASE_URL}/edf/files`, {
            //     headers: { Authorization: `Bearer ${token}` }
            // });
            // setEdfFiles(response.data || []);
            
            // Simulação de dados de arquivos EDF:
            console.log("Buscando arquivos EDF (simulado)...");
            setTimeout(() => {
                const mockFiles = [
                    { id: 1, filename: "test_01.edf", upload_timestamp: new Date().toISOString(), processing_status: "COMPLETED" },
                    { id: 2, filename: "subject_alpha.edf", upload_timestamp: new Date().toISOString(), processing_status: "PROCESSING" },
                    { id: 3, filename: "recording_xyz.edf", upload_timestamp: new Date().toISOString(), processing_status: "UPLOADED" },
                ];
                setEdfFiles(mockFiles);
                // Inicializar status de processamento
                const initialStatus = {};
                mockFiles.forEach(f => { initialStatus[f.id] = f.processing_status; });
                setProcessingStatus(initialStatus);
            }, 500);

        } catch (error) {
            console.error("Erro ao buscar arquivos EDF:", error);
            // Tratar erro (ex: se token expirou, redirecionar para login)
            if (error.response && error.response.status === 401) {
                handleLogout(); // Deslogar se não autorizado
            }
        }
    };
    
    // Chamar a API do backend (exemplo: endpoint raiz)
    useEffect(() => {
        axios.get(`${API_BASE_URL}/`)
            .then(response => {
                setMessage(response.data.message || "Conectado ao backend!");
            })
            .catch(error => {
                console.error("Erro ao conectar com o backend:", error);
                setMessage("Falha ao conectar com o backend. Verifique se está rodando.");
            });

        if (authToken) {
            fetchEdfFiles(authToken);
        }
    }, [authToken]); // Executa quando authToken muda


    // Simulação de atualização de status de processamento (via polling ou WebSocket)
    useEffect(() => {
        if (!selectedEdfId || !authToken) return;

        // Apenas simula para arquivos que não estão 'COMPLETED' ou 'FAILED'
        if (processingStatus[selectedEdfId] && 
            (processingStatus[selectedEdfId] === 'COMPLETED' || processingStatus[selectedEdfId] === 'FAILED')) {
            return;
        }

        const interval = setInterval(() => {
            // Em uma aplicação real:
            // 1. WebSocket: ouvir por mensagens do servidor sobre o status do selectedEdfId.
            // 2. Polling: fazer uma chamada API para buscar o status atualizado do selectedEdfId.
            //    Ex: axios.get(`${API_BASE_URL}/edf/files/${selectedEdfId}/status`, { headers: { Authorization: `Bearer ${authToken}` }})
            //        .then(response => setProcessingStatus(prev => ({...prev, [selectedEdfId]: response.data.status })));

            console.log(`Simulando verificação de status para o arquivo ${selectedEdfId}... Estado atual: ${processingStatus[selectedEdfId]}`);
            // Simulação de progressão de status
            setProcessingStatus(prevStatus => {
                const current = prevStatus[selectedEdfId];
                let nextStatus = current;
                if (current === "UPLOADED") nextStatus = "PREPROCESSING";
                else if (current === "PREPROCESSING") nextStatus = "ICA_PROCESSING";
                else if (current === "ICA_PROCESSING") nextStatus = "FEATURE_EXTRACTION";
                else if (current === "FEATURE_EXTRACTION") nextStatus = "COMPLETED";
                
                if (nextStatus !== current) {
                     console.log(`Status do arquivo ${selectedEdfId} mudou para: ${nextStatus}`);
                     // Em uma app real, se COMPLETED, poderia buscar os resultados/features.
                }
                return { ...prevStatus, [selectedEdfId]: nextStatus };
            });

        }, 5000); // Verifica a cada 5 segundos

        return () => clearInterval(interval); // Limpa o intervalo ao desmontar ou se selectedEdfId mudar
    }, [selectedEdfId, authToken, processingStatus]);


    const handleFileSelect = (fileId) => {
        setSelectedEdfId(fileId);
        console.log(`Arquivo selecionado: ${fileId}`);
    };
    
    // Simulação de upload de arquivo
    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;
        if (!authToken) {
            alert("Faça login para enviar arquivos.");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            // const response = await axios.post(`${API_BASE_URL}/edf/upload`, formData, {
            //     headers: {
            //         'Content-Type': 'multipart/form-data',
            //         Authorization: `Bearer ${authToken}`,
            //     },
            //     onUploadProgress: progressEvent => {
            //         const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            //         console.log(`Upload progress: ${percentCompleted}%`);
            //         // TODO: Atualizar UI com progresso de upload
            //     }
            // });
            // console.log("Upload bem-sucedido (simulado):", response.data);
            // alert(`Arquivo ${response.data.filename} enviado! ID: ${response.data.file_id}`);
            // fetchEdfFiles(authToken); // Re-busca a lista de arquivos
            
            // Simulação:
            console.log(`Simulando upload do arquivo: ${file.name}`);
            alert(`Simulação: Arquivo ${file.name} enviado. Em uma app real, isso iria para o backend.`);
            // Adicionar à lista mockada para visualização (apenas simulação)
            const newFileId = Math.max(0, ...edfFiles.map(f => f.id)) + 1;
            const newFile = { id: newFileId, filename: file.name, upload_timestamp: new Date().toISOString(), processing_status: "UPLOADED" };
            setEdfFiles(prev => [...prev, newFile]);
            setProcessingStatus(prev => ({...prev, [newFileId]: "UPLOADED"}));


        } catch (error) {
            console.error("Erro no upload do arquivo (simulado):", error);
            alert("Falha no upload do arquivo (simulado). Verifique o console.");
        }
    };


    return (
        <div className="App">
            <header className="App-header">
                <h1>Plataforma de Análise EEG</h1>
                <p>Backend status: {message}</p>
                {!authToken ? (
                    <button onClick={() => handleLogin("user@example.com", "password")}>
                        Login Simulado
                    </button>
                ) : (
                    <button onClick={handleLogout}>Logout Simulado</button>
                )}
            </header>

            {authToken && (
                <section className="App-content">
                    <div className="file-management">
                        <h2>Meus Arquivos EDF</h2>
                        <input type="file" accept=".edf" onChange={handleFileUpload} />
                        {edfFiles.length === 0 && <p>Nenhum arquivo encontrado.</p>}
                        <ul>
                            {edfFiles.map(file => (
                                <li 
                                    key={file.id} 
                                    onClick={() => handleFileSelect(file.id)}
                                    className={selectedEdfId === file.id ? 'selected' : ''}
                                >
                                    {file.filename} (Status: {processingStatus[file.id] || file.processing_status || 'N/A'})
                                    {selectedEdfId === file.id && processingStatus[file.id] !== 'COMPLETED' && processingStatus[file.id] !== 'FAILED' && <span> (Verificando...)</span>}
                                </li>
                            ))}
                        </ul>
                    </div>
                    
                    <div className="eeg-visualization">
                        <h2>Visualização do Sinal</h2>
                        {selectedEdfId ? (
                            <EEGPlot edfFileId={selectedEdfId} />
                        ) : (
                            <p>Selecione um arquivo EDF para visualizar o sinal.</p>
                        )}
                        {selectedEdfId && processingStatus[selectedEdfId] && (
                            <p>Status do Processamento (Arquivo {selectedEdfId}): <strong>{processingStatus[selectedEdfId]}</strong></p>
                        )}
                    </div>
                </section>
            )}
        </div>
    );
}

export default App;
