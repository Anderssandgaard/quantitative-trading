%% calculate shape ratio
addpath(genpath(cd))
%% Anders Dyhr Sandgaard
clear
% Example Call: Fetching AMD stock data
symbol = 'IGE';
start_dt = '26-Feb-2024';
end_dt = '14-Nov-2025'; 
interval = '1h';% typical options: '1m', '2m', '5m', '15m', , '1h', '1d'
try
    amdData = getMarketDataViaYahoo(symbol, start_dt, end_dt, interval);
    if isempty(amdData)
        error('Data does not exist. modify interval and/or date')
        return
    end
    % Display the first few rows
    disp('Successfully retrieved data:')
    head(amdData)
    
    % Quick visualization
    figure;
    plot(amdData.Date, amdData.Close, 'LineWidth', 1.5);
    grid on;
    title(['Stock Price History: ', symbol]);
    xlabel('Date');
    ylabel('Closing Price (USD)');
    
    %Annualized Sharpe ratio
    results = sharpe_ratio_all(amdData.AdjClose, amdData.Date)  
catch ME
    fprintf('Error: %s\n', ME.message);
end
%% Maximum drawdown and maximum drawdown duration




