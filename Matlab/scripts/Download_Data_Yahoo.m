%% Download data from Yahoo
addpath(genpath(cd))
%% Anders Dyhr Sandgaard
clc
% Example Call: Fetching AMD stock data
symbol = 'AAPL';
start_dt = '1-Feb-2010';
end_dt = '7-Feb-2026'; % Today
interval = '1m'; %
try
    amdData = getMarketDataViaYahoo(symbol, start_dt, end_dt, interval);
    
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
    
catch ME
    fprintf('Error: %s\n', ME.message);
end


