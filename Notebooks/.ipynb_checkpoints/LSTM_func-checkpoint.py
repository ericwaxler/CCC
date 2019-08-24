def LSTM_model(lookbehind, train_ratio, df):
    #importing required libraries
    from sklearn.preprocessing import MinMaxScaler
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout, LSTM
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    data = df.sort_index(ascending=True, axis=0)
    new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'Close'])
    for i in range(0,len(data)):
        new_data['Date'][i] = data['Date'][i]
        new_data['Close'][i] = data['Close'][i]

    #previous days to use for prediction
    #lookbehind = 60
    #train_ratio = .9
    num_samples = len(df)
    train_samples = int(train_ratio * num_samples)

    #setting index
    new_data.index = new_data.Date
    new_data.drop('Date', axis=1, inplace=True)

    #creating train and test sets
    dataset = new_data.values

    train = dataset[0:train_samples,:]
    valid = dataset[train_samples:,:]

    #converting dataset into x_train and y_train
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    x_train, y_train = [], []
    for i in range(lookbehind,len(train)):
        x_train.append(scaled_data[i-lookbehind:i,0])
        y_train.append(scaled_data[i,0])
    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

    # create and fit the LSTM network
    model4 = Sequential()
    model4.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model4.add(LSTM(units=50))
    model4.add(Dense(1))

    model4.compile(loss='mean_squared_error', optimizer='adam')
    model4.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)

    #predicting 246 values, using past 60 from the train data
    inputs = new_data[len(new_data) - len(valid) - lookbehind:].values
    inputs = inputs.reshape(-1,1)
    inputs  = scaler.transform(inputs)

    X_test = []
    for i in range(lookbehind,inputs.shape[0]):
        X_test.append(inputs[i-lookbehind:i,0])
    X_test = np.array(X_test)

    X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
    closing_price = model4.predict(X_test)
    closing_price = scaler.inverse_transform(closing_price)

    rms=np.sqrt(np.mean(np.power((valid-closing_price),2)))

    train = new_data[:train_samples]
    valid = new_data[train_samples:]
    valid['Predictions'] = closing_price

    #plt.plot(train['Close'])
    plt.figure(figsize=(19,8))
    plt.plot(valid[['Close','Predictions']])
    plt.legend(['Actual','Predicted'])
    plt.title(str(lookbehind) + ' Day Interval, ' + ('{0:.0%}'.format(train_ratio)) + ' Train Split')

    plt.figure(figsize=(19,8))
    plt.plot(valid[['Close','Predictions']].tail(21))
    plt.legend(['Actual','Predicted'])
    plt.title(str(lookbehind) + ' Day Interval, ' + ('{0:.0%}'.format(train_ratio)) + ' Train Split')
    
    plt.figure(figsize=(19,8))
    plt.plot(valid['Close'].tail(21)-valid['Predictions'].tail(21))
    plt.legend(['Actual - Predicted'])
    plt.title('Residual: ' + str(lookbehind) + ' Day Interval, ' + ('{0:.0%}'.format(train_ratio)) + ' Train Split')