%% Download data from Yahoo
%% Anders Dyhr Sandgaard

function data = getMarketDataViaYahoo(symbol, startdate, enddate, interval)
    % Default values
    if nargin < 4, interval = '1d'; end
    if nargin < 3, enddate = datetime('now'); end
    if nargin < 2, startdate = datetime('now') - days(365); end
    
    start_dt = datetime(startdate);
    now_dt = datetime('now');
    
    % --- SMART ADJUSTMENT BLOCK ---
    days_diff = days(now_dt - start_dt);
    if strcmp(interval, '1m') && days_diff > 7
        start_dt = now_dt - days(7);
    elseif ismember(interval, {'2m', '5m', '15m', '30m', '90m'}) && days_diff > 60
        start_dt = now_dt - days(60);
    elseif (strcmp(interval, '1h') || strcmp(interval, '60m')) && days_diff > 730
        start_dt = now_dt - days(730);
    end

    p1 = num2str(posixtime(start_dt), '%.0f');
    p2 = num2str(posixtime(datetime(enddate)), '%.0f');
    
    baseUrl = sprintf('https://query1.finance.yahoo.com/v8/finance/chart/%s', upper(symbol));
    uri = matlab.net.URI(baseUrl, 'period1', p1, 'period2', p2, 'interval', interval);

    options = matlab.net.http.HTTPOptions('ConnectTimeout', 20);
    header = matlab.net.http.HeaderField('User-Agent', 'Mozilla/5.0');
    request = matlab.net.http.RequestMessage('GET', header);
    
    response = request.send(uri, options);
    
    try
        res = response.Body.Data.chart.result;
        % Ensure we are working with column vectors
        t = datetime(res.timestamp, 'ConvertFrom', 'posixtime', 'TimeZone', 'local')';
        q = res.indicators.quote;
        
        % Extract prices
        O = q.open'; H = q.high'; L = q.low'; C = q.close'; V = q.volume';
        
        % AdjClose is sometimes in a nested struct
        if isfield(res.indicators, 'adjclose')
            AC = res.indicators.adjclose.adjclose';
        else
            AC = C; % Fallback to Close if AdjClose isn't provided
        end
        
        data = table(t, O, H, L, C, AC, V, ...
            'VariableNames', {'Date', 'Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume'});
            
    catch
        warning('Could not parse data for %s. Check if symbol is correct.', symbol);
        data = table();
    end
end