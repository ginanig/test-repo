// frontend/src/components/EEGPlot.js
import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

const EEGPlot = ({ edfFileId }) => {
    const [data, setData] = useState([]);
    const [layout, setLayout] = useState({
        title: 'Sinal EEG (Mock Data)',
        xaxis: { title: 'Tempo (s)' },
        yaxis: { title: 'Amplitude (µV)' },
        height: 400,
        // width: 800, // Removido para ser responsivo
        autosize: true,
        showlegend: true,
    });
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (edfFileId) {
            // TODO: Implementar busca de dados do EEG para o edfFileId
            // Por enquanto, usando dados mockados
            console.log(`EEGPlot: Simulating data fetch for edfFileId: ${edfFileId}`);
            setLoading(true);
            setTimeout(() => {
                const mockChannels = ['Cz', 'Pz', 'Fz'];
                const time = Array.from({ length: 200 }, (_, i) => i * 0.01); // 2 segundos de dados a 100Hz
                
                const plotData = mockChannels.map(channelName => ({
                    x: time,
                    y: Array.from({ length: 200 }, () => Math.random() * 20 - 10), // Dados aleatórios
                    type: 'scattergl', // 'scattergl' para melhor performance com muitos pontos
                    mode: 'lines',
                    name: channelName,
                }));
                setData(plotData);
                setLayout(prevLayout => ({ ...prevLayout, title: `Sinal EEG para Arquivo ${edfFileId} (Mock Data)`}));
                setLoading(false);
            }, 1000);
        } else {
            // Dados mockados iniciais se nenhum arquivo for selecionado
            const time = Array.from({ length: 100 }, (_, i) => i * 0.01);
            setData([{
                x: time,
                y: time.map(t => Math.sin(t * 2 * Math.PI * 5) * 10), // Onda senoidal de 5Hz
                type: 'scattergl',
                mode: 'lines',
                name: 'Canal Mock 1',
            }]);
            setLayout(prevLayout => ({ ...prevLayout, title: 'Sinal EEG (Mock Data Inicial)'}));
        }
    }, [edfFileId]); // Re-executa quando edfFileId muda

    if (error) {
        return <div style={{color: 'red'}}>Erro ao carregar dados do gráfico: {error}</div>;
    }

    return (
        <div style={{ width: '100%', overflow: 'hidden' }}>
            {loading && <p>Carregando dados do gráfico...</p>}
            <Plot
                data={data}
                layout={layout}
                useResizeHandler={true} // Permite que o gráfico se redimensione com a janela
                style={{ width: '100%', height: '100%' }}
                config={{ responsive: true }} // Garante responsividade
            />
        </div>
    );
};

export default EEGPlot;
