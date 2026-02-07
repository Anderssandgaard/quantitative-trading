function results = sharpe_ratio_all(cls_adj, Date)
% SHARPE_RATIO_ALL  Calculate annualized Sharpe Ratios across multiple timeframes.
%
% USAGE:
%   results = sharpe_ratio_all(price_array, date_array)
%
% INPUTS:
%   cls_adj - Vector of Adjusted Closing prices
%   Date    - Vector of datetime objects corresponding to cls_adj
%
% OUTPUT:
%   results - Struct containing Daily, Hourly, and Minute Sharpe Ratios

    %% 1. Configuration & Data Heartbeat
    % Detect the median gap in minutes to understand what data we have
    base_gap  = minutes(median(diff(Date)));
    % Identify Market Type: If trades exist on weekends, it's 24/7 (Crypto)
 
    is_crypto = any(isweekend(Date));
    daily_min = ifelse(is_crypto, 1440, 390);
    % Define the Tier Parameters
    % target_mins: The bar size we want to analyze
    % shift_unit:  MATLAB's dateshift keyword
    % field_name:  The label for our results struct
    target_mins = [daily_min, 60, 1];
    if base_gap>390, base_gap = daily_min;end

    shift_unit  = {'day', 'hour', 'minute'};
    field_name  = {'Daily', 'Hourly', 'Minute'};
    
    results = struct();

    %% 2. Processing Tiers
    % We loop through each resolution and "downsample" if possible
    for i = 1:length(field_name)
        
        % Check if the requested tier is larger than our data granularity
        % (e.g., We can't calculate 1-minute Sharpe from 1-hour data)
        if target_mins(i) >= (base_gap - 0.1)
            
            % --- EXPLICIT SAMPLING ---
            % Find indices for the LAST available price in each time bucket
            [~, ind] = unique(dateshift(Date, "start", shift_unit{i}), 'last');
            
            % Extract the sampled prices
            tiered_prices = cls_adj(ind);
            
            % --- MATH EXECUTION ---
            results.(field_name{i}) = calculate_sharpe(tiered_prices, target_mins(i), is_crypto);
        else
            % If data is too coarse (e.g., trying to get 1m Sharpe from 1d data)
            results.(field_name{i}) = NaN; 
        end
    end
end

%% --- HELPER FUNCTIONS ---

function s = calculate_sharpe(prices, mins, is_crypto)
% Calculates the annualized Sharpe Ratio for a specific price vector
    
    rf_annual = 0.04; % Assumed 4% Risk-Free Rate
    
    % 1. Determine Annualization Factor (N)
    % N represents the total number of these 'mins' periods in one year
    if is_crypto
        N = (365 * 1440) / mins;
    else
        % 252 trading days * 6.5 hours/day * 60 mins/hour = 98,280 mins
        N = (252 * 390) / mins;
    end
    
    % 2. Calculate Simple Returns
    returns = (prices(2:end) - prices(1:end-1)) ./ prices(1:end-1);
    
    % Basic safety check for data length
    if length(returns) < 2
        s = NaN; return;
    end
    
    % 3. Calculate Risk-Adjusted Return
    rf_period = rf_annual / N;
    excess_returns = returns - rf_period;
    
    % 4. Compute Annualized Sharpe Ratio
    % (Mean Excess Return / Volatility) * Square Root of Time
    s = (mean(excess_returns,'omitnan') / std(excess_returns,[],'omitnan')) * sqrt(N);
end

function val = ifelse(cond, t, f)
% Simple ternary-style logic for cleaner assignments
    if cond, val = t; else, val = f; end
end