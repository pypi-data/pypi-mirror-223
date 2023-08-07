def main():
    import tkinter as tk
    from tkinter import messagebox
    import sys
    import datetime
    import psutil
    from PIL import Image, ImageTk
    import platform
    import time

    def bekle(n):
        time.sleep(n)

    def login():
        username = entry_username.get()
        password = entry_password.get()

        if username == "Aras" and password == "Aras.123!":
            messagebox.showinfo("Başarılı", "Giriş başarılı!")
            window.withdraw()
            open_main_page()
        else:
            messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya parola!")

    def python():
        class RedirectedOutput:
            def __init__(self, output_text):
                self.output_text = output_text

            def write(self, message):
                self.output_text.configure(state="normal")
                self.output_text.insert(tk.END, message)
                self.output_text.configure(state="disabled")
                self.output_text.see(tk.END)

        def execute_command():
            command = input_text.get("1.0", tk.END).strip()
            try:
                result = eval(command)
                print(result)
            except Exception as e:
                print(str(e))
            input_text.delete("1.0", tk.END)

        def exit_console():
            sys.exit()

        root = tk.Tk()
        root.title("Python Konsolu")
        root.attributes("-topmost", True)
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        input_text = tk.Text(input_frame, width=60, height=5)  # Yükseklik ayarı burada yapılıyor
        input_text.pack(side=tk.LEFT)

    #    execute_button = tk.Button(input_frame, text="Çalıştır", command=execute_command)
    #    execute_button.pack(side=tk.LEFT, padx=10)
        output_text = tk.Text(root, width=60, height=20)
        output_text.pack()

        exit_button = tk.Button(root, text="Çalıştır", command=execute_command)
        exit_button.pack(pady=10)

        # Çıktıyı yönlendir
        sys.stdout = RedirectedOutput(output_text)

        root.mainloop()

    def system_infos():
        def get_system_info():
        # İşletim sistemi bilgilerini al
            os_name = platform.system()
            os_version = platform.release()

            # İşlemci bilgilerini al
            processor = platform.processor()

            # Bellek bilgilerini al
            memory = psutil.virtual_memory()

            # Ekran çözünürlüğünü al
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            screen_resolution = f"{screen_width}x{screen_height}"

            # Bilgileri canvas üzerinde yazdır
            canvas.delete("all")
            canvas.create_text(200, 25, text="Donanım Bilgileri", font=("Arial", 14, "bold"), anchor="n")
            canvas.create_text(200, 50, text=f"İşletim Sistemi: {os_name} {os_version}", anchor="n")
            canvas.create_text(200, 75, text=f"İşlemci: {processor}", anchor="n")
            canvas.create_text(200, 100, text=f"Bellek: {memory.total // (1024 ** 3)} GB", anchor="n")
            canvas.create_text(200, 125, text=f"Ekran Çözünürlüğü: {screen_resolution}", anchor="n")

        def get_other_info():
            # Diğer verileri al ve canvas üzerinde yazdır (örneğin, kullanıcı adı, IP adresi, vb.)
            # Bu kısmı kendi ihtiyaçlarınıza göre düzenleyebilirsiniz
            canvas.create_text(200, 175, text="Diğer Bilgiler", font=("Arial", 14, "bold"), anchor="n")
            canvas.create_text(200, 200, text="Kullanıcı Adı: John Doe", anchor="n")
            canvas.create_text(200, 225, text="IP Adresi: 192.168.1.1", anchor="n")

        root = tk.Tk()
        root.title("Bilgisayar Bilgileri")

        # Canvas
        canvas = tk.Canvas(root, width=400, height=250)
        canvas.pack()
        root.attributes("-topmost", True)
        # Donanım bilgilerini al butonu
        button_get_system_info = tk.Button(root, text="Donanım Bilgilerini Al", command=get_system_info)
        button_get_system_info.pack(pady=10)

        # Diğer bilgileri al butonu
        button_get_other_info = tk.Button(root, text="Diğer Bilgileri Al", command=get_other_info)
        button_get_other_info.pack(pady=10)

        root.mainloop()

    def browser():
        import tkinter as tk
        from PyQt5.QtCore import QUrl, Qt
        from PyQt5.QtWidgets import QApplication, QMainWindow
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        import sys

        class WebBrowser(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("Tarayıcı")
                self.setGeometry(100, 100, 800, 600)

                self.web_view = QWebEngineView()
                self.setCentralWidget(self.web_view)

            def load_url(self, url):
                self.web_view.load(QUrl(url))
                self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Pencerenin en üstte kalmasını sağlar
                self.show()
                self.activateWindow()  # Pencereyi etkinleştirir

        def open_browser():
            app = QApplication(sys.argv)
            browser = WebBrowser()
            browser.show()
            app.exec_()

        root = tk.Tk()
        root.title("Web Tarayıcısı")
        #root.attributes("-fullscreen", True) 

        label = tk.Label(root, text="URL:")
        label.pack()

        entry = tk.Entry(root, width=50)
        entry.pack()

        button = tk.Button(root, text="Aç", command=open_browser)
        button.pack()

        root.mainloop()


    def google():
        from PyQt5.QtCore import QUrl, Qt
        from PyQt5.QtWidgets import QApplication, QMainWindow
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        import sys

        class WebBrowser(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("Tarayıcı")
                self.setGeometry(100, 100, 800, 600)

                self.web_view = QWebEngineView()
                self.setCentralWidget(self.web_view)

            def load_url(self, url):
                self.web_view.load(QUrl(url))
                self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Pencerenin en üstte kalmasını sağlar
                self.show()
                self.activateWindow()  # Pencereyi etkinleştirir

                # Web tarayıcısını açmak için
        app = QApplication(sys.argv)
        browser = WebBrowser()
        browser.load_url("https://www.google.com")  # Görüntülemek istediğiniz URL'yi buraya yazın
        browser.show()
        app.exec_()
    
    def notepad():
        def yeni_dosya():
            metin_alani.delete(1.0, tk.END)

        def dosya_ac():
            dosya_yolu = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Metin Dosyaları", "*.txt"), ("Tüm Dosyalar", "*.*")])
            if dosya_yolu:
                with open(dosya_yolu, "r") as dosya:
                    metin = dosya.read()
                    metin_alani.delete(1.0, tk.END)
                    metin_alani.insert(tk.END, metin)

        def dosya_kaydet():
            dosya_yolu = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Metin Dosyaları", "*.txt"), ("Tüm Dosyalar", "*.*")])
            if dosya_yolu:
                with open(dosya_yolu, "w") as dosya:
                    dosya.write(metin_alani.get(1.0, tk.END))

        # Pencere oluşturma
        pencere = tk.Tk()
        pencere.title("Basit Not Defteri")

        # Metin alanı (Text widget)
        metin_alani = tk.Text(pencere, wrap="word")
        metin_alani.pack(expand=True, fill="both")

        # Menü çubuğu oluşturma
        menu_cubugu = tk.Menu(pencere)
        pencere.config(menu=menu_cubugu)

        # Dosya menüsü
        dosya_menu = tk.Menu(menu_cubugu, tearoff=False)
        menu_cubugu.add_cascade(label="Dosya", menu=dosya_menu)
        dosya_menu.add_command(label="Yeni", command=yeni_dosya)
        dosya_menu.add_command(label="Aç", command=dosya_ac)
        dosya_menu.add_command(label="Kaydet", command=dosya_kaydet)
        dosya_menu.add_separator()
        dosya_menu.add_command(label="Çıkış", command=pencere.quit)

        # Yeni butonu
        yeni_buton = tk.Button(pencere, text="Yeni", command=yeni_dosya)
        yeni_buton.pack(side=tk.LEFT, padx=5, pady=5)

        # Aç butonu
        ac_buton = tk.Button(pencere, text="Aç", command=dosya_ac)
        ac_buton.pack(side=tk.LEFT, padx=5, pady=5)

        # Kaydet butonu
        kaydet_buton = tk.Button(pencere, text="Kaydet", command=dosya_kaydet)
        kaydet_buton.pack(side=tk.LEFT, padx=5, pady=5)

        # Uygulamayı çalıştırma
        pencere.mainloop()

    def wix():
        import random
        import time
        import wikipedia
        from getpass import getpass
        import socket
        import string
        import os
        import tkinter as tk
        import sys

        class RedirectedOutput:
                def __init__(self, output_text):
                    self.output_text = output_text

                def write(self, message):
                    self.output_text.configure(state="normal")
                    self.output_text.insert(tk.END, message)
                    self.output_text.configure(state="disabled")
                    self.output_text.see(tk.END)

        responses = {
                "merhaba": "Merhaba, nasıl yardımcı olabilirim?",
                "sa": "as",
                "nasılsınız": "Ben bir algoritma olduğum için hissetmiyorum, ama teşekkür ederim, iyiyim!",
                "naber": "Ben bir algoritma olduğum için hissetmiyorum, ama teşekkür ederim, iyiyim!",
                "güle güle": "Hoşça kalın!",
                "teşekkür ederim": "Rica ederim, yardımcı olabildiysem ne mutlu bana!",
                "diğerleri": "Üzgünüm, bu konuda henüz bilgim yok. Başka bir soru sormak ister misiniz?",
                "python öğrenmek istiyorum": "Python öğrenmek harika bir seçim! Başlamak için online kaynaklara göz atabilirsiniz, Python öğrenmeye başlamak için birçok ücretsiz kaynak bulunmaktadır. İyi bir başlangıç noktası olarak Python belgelerine bakabilirsiniz.",
                "programlama dilleri": "Programlama dilleri, yazılım geliştirme için kullanılan araçlardır. Bazı popüler programlama dilleri Python, Java, C++, JavaScript, Ruby vb. şeklinde sıralanabilir. Programlama dilleri, bilgisayarlara talimatlar vermek ve yazılım oluşturmak için kullanılan yapılardır. Her dilin kendine özgü özellikleri ve kullanım alanları vardır.",
                "yapay zeka nedir": "Yapay zeka, bilgisayar sistemlerinin insan benzeri zekaya sahip olmasını amaçlayan bir alanı ifade eder. Makine öğrenmesi, derin öğrenme, doğal dil işleme gibi teknikler kullanarak bilgisayarların öğrenme, anlama ve karar verme yetenekleri geliştirilmeye çalışılır. Yapay zeka, bilgisayar sistemlerine insan benzeri zeka ve öğrenme yetenekleri kazandırmayı hedefleyen bir alandır. Bu alanda pek çok yöntem ve teknik bulunur ve çeşitli uygulamalarda kullanılır."
        }

        sakalar = [
                "İki balık yüzmüş, biri düşmüş. Diğeri ne demiş? Hadi çık, balık tutalım!",
                "Temel, doktora gitmiş. Doktor: Sigarayı bırakmazsan ömrünü yarı yarıya kaybedersin. demiş. Temel: Doktor bey, ben zaten paketin yarısını içiyorum!",
                "Bir bankaya giren hırsız, kasada ne olduğunu sormuş. Banka görevlisi: Sevgi var. demiş. Hırsız: E peki, bana biraz sevgi verin o zaman!",
                "Bir matematikçi kahveye gitmiş, garsona demiş ki: Bana bir kahve getir, lütfen, sonsuzluğa kadar şekersiz. Garson: Sonsuzluğa kadar şekersiz mi? demiş. Matematikçi gülümseyerek cevaplamış: Evet, çünkü sonsuz artı bir değişmez!",
                "Nasrettin Hoca'ya sormuşlar: Hocam, dünya dönüyor mu? Hoca yanıtlamış: Dönüyor tabii ki, bir gün bir yöne, bir gün başka bir yöne.",
                "Bir tavuk yolda yürürken şöyle demiş: Eğer yolun karşısına geçebilirsem, neden yürüyorum ki?"
        ]

        def bekle(n):
            time.sleep(n)


        def get_wikipedia_summary(keyword):
                import wikipedia
                try:
                    summary = wikipedia.summary(keyword)
                    return summary
                except wikipedia.exceptions.DisambiguationError as e:
                    # Eğer birden fazla anlamı varsa, ilk anlamı döndürebilirsiniz
                    summary = wikipedia.summary(e.options[0])
                    return summary
                except wikipedia.exceptions.PageError:
                    # Sayfa bulunamadı hatası
                    return "Aradığınız konu Wikipedia'da bulunamadı."

        def execute_command():
            command = input_text.get("1.0", tk.END).strip()
            try:
                result = eval(command)
                print(result)
            except Exception as e:
                print(str(e))
            input_text.delete("1.0", tk.END)
            if command in responses:
                    print("Wix: " + responses[command])
            elif "wikipedia" in command or "wiki" in command:
                    wikipedia = "wikipedia"
                    sentence2 = command.replace(wikipedia, "")
                    get_wikipedia_summary(sentence2)
                    summary = get_wikipedia_summary(sentence2)
                    print(summary)
            elif "şifre oluştur" in command or "sifrele" in command or "şifre yaz" in command or "şifre" in command:

                    chars = string.ascii_letters + string.digits + string.punctuation
                    rand_kucuk = random.randint(0,25)
                    rand_buyuk = random.randint(26,31)
                    rand_rakam = random.randint(32,41)
                    rand_isaret = random.randint(42,73)
                    rand_all = random.randint(26,31)
                    rand_all2 = random.randint(0,73)
                    rand_all3 = random.randint(42,73)
                    rand_all4 = random.randint(0,73)

                    sifre = chars[rand_buyuk] + chars[rand_rakam] + chars[rand_kucuk] + chars[rand_isaret] + chars[rand_all] + chars[rand_all2] + chars[rand_all3] + chars[rand_all4]
                    print("Wix: 8 haneli şifreniz oluşturuluyor, lütfen bekleyiniz.")
                    bekle(1)
                    print(sifre)

            elif "fake generator" in command or "info generator" in command or "fake info generator" in command or "fake info" in command or "fake infos" in command:
                    from faker import Faker

                    fake = Faker()
                    profile = fake.profile()
                    print(profile)
            elif "lstm data" in command:
                            import csv
                            import datetime
                            import cryptocompare

                            input1 = input("Geçimiş değerlerini çekmek istediğiniz kripto paranın sembolik adını yazınız örneğin 'BTC': ")
                            date_input = input("\nVeri setinde olmasını istediğiniz son tarihi sayıların arasına "+"'.' "+"yerine "+"'-' "+"koyarak tarih,ay,gün sırasıyla yazınız yazınız. örneğin 2023-10-01: " )
                            def get_historical_btc_price(start_date, end_date):
                                historical_data = cryptocompare.get_historical_price_day(input1, currency='USD', toTs=datetime.datetime.strptime(end_date, '%Y-%m-%d'))
                                prices = []
                                for data in historical_data:
                                    date = datetime.datetime.fromtimestamp(data['time']).strftime('%Y-%m-%d')
                                    price = data['close']
                                    prices.append((date, price))
                                    if date == start_date:
                                        break
                                return prices

                            # Örnek kullanım
                            start_date = date_input
                            end_date = date_input
                            historical_prices = get_historical_btc_price(start_date, end_date)

                            # CSV dosyasına yazma
                            filename1 = input1+'_prices.csv'
                            with open(filename1, 'w', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Date', 'Close'])
                                writer.writerows(historical_prices)

                            print(input1+f" değerleri '{filename1}' dosyasına kaydedildi.")

            elif "lstm" in command:
                            import numpy as np
                            import pandas as pd
                            import matplotlib.pyplot as plt
                            import tensorflow as tf
                            from sklearn.preprocessing import MinMaxScaler
                            from sklearn.metrics import mean_squared_error
                            from tensorflow.keras.models import Sequential
                            from tensorflow.keras.layers import LSTM, Dropout, Dense
                            from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
                            
                            inputdf = input("Veri setinin giriniz: ")
                            # Veri setini yükle
                            df = pd.read_csv(inputdf)

                            # Veri setini incele
                            def check_df(dataframe, head=5):
                                print("******************** SHAPE ********************")
                                print(dataframe.shape)
                                print("******************** TYPES ********************") 
                                print(dataframe.dtypes)
                                print("******************** HEAD ********************")
                                print(dataframe.head(head))
                                print("******************** TAIL ********************") 
                                print(dataframe.tail(head))
                                print("******************** NA ********************") 
                                print(dataframe.isnull().sum())

                            check_df(df)

                            # Tarih sütununu datetime formatına dönüştür
                            df['Date'] = pd.to_datetime(df['Date'])

                            # Kapanış fiyatını içeren sütunu seç
                            tesla_df = df[['Date', 'Close']]

                            # Veri setinin başlangıç ve bitiş tarihlerini kontrol et
                            print("Maximum Tarih: ", tesla_df['Date'].max())
                            print("Minimum Tarih: ", tesla_df['Date'].min())
                            print("Maximum Kapanış: ", tesla_df['Close'].max())
                            print("Minimum Kapanış: ", tesla_df['Close'].min())

                            # Tarih sütununu indeks olarak ayarla
                            tesla_df.set_index('Date', inplace=True)

                            # Veri setini görselleştir
                            #plt.figure(figsize=(12, 6))
                            #plt.plot(tesla_df['Close'], color='blue')
                            #plt.ylabel('Stock Price')
                            #plt.title('Bitcoin Stock Price')
                            #plt.xlabel('Time')
                            #plt.show()

                            # Veri setini ölçeklendir
                            scaler = MinMaxScaler(feature_range=(0, 1))
                            scaled_data = scaler.fit_transform(tesla_df)

                            # Eğitim ve test veri setlerini oluştur
                            train_size = int(len(scaled_data) * 0.8)
                            train_data = scaled_data[:train_size]
                            test_data = scaled_data[train_size:]

                            # Veri setini özelliklere ve hedef değişkene ayır
                            def create_features(data, lookback):
                                X, y = [], []
                                for i in range(lookback, len(data)):
                                    X.append(data[i-lookback:i, 0])
                                    y.append(data[i, 0])
                                return np.array(X), np.array(y)

                            lookback = 4
                            X_train, y_train = create_features(train_data, lookback)
                            X_test, y_test = create_features(test_data, lookback)

                            # Veri setinin şekillerini yeniden düzenle
                            X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
                            X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

                            # Modeli oluştur
                            #model = Sequential()
                            #model.add(LSTM(units=50, activation='relu', input_shape=(X_train.shape[1], 1)))
                            #model.add(Dropout(0.2))
                            #model.add(Dense(1))

                            model = Sequential()
                            model.add(LSTM(units=50, activation='relu', input_shape=(X_train.shape[1], 1), return_sequences=True))
                            model.add(LSTM(units=50, activation='relu', return_sequences=True))
                            model.add(LSTM(units=50, activation='relu'))
                            model.add(Dropout(0.2))
                            model.add(Dense(1))
                            model.summary()
                            # Modeli derle
                            model.compile(loss='mean_squared_error', optimizer='adam')

                            filep = "lstm_model_1"
                            # Modeli eğitim sürecini tanımla
                            callbacks = [EarlyStopping(monitor='val_loss', patience=3, verbose=1, mode='min'),
                                        ModelCheckpoint(filepath=filep, monitor='val_loss', mode='min',
                                                        save_best_only=True, save_weights_only=False, verbose=1)]

                            # Modeli eğit
                            history = model.fit(X_train, y_train, epochs=123, batch_size=37,
                                                validation_data=(X_test, y_test), callbacks=callbacks, shuffle=False)

                            # Modelin performansını değerlendir
                            train_predict = model.predict(X_train)
                            test_predict = model.predict(X_test)

                            # Ölçeklemeyi tersine çevirerek tahminleri gerçek değerlere dönüştür
                            train_predict = scaler.inverse_transform(train_predict)
                            test_predict = scaler.inverse_transform(test_predict)

                            # RMSE değerlerini hesapla
                            train_rmse = np.sqrt(mean_squared_error(tesla_df[lookback:train_size], train_predict))
                            test_rmse = np.sqrt(mean_squared_error(tesla_df[train_size + lookback:], test_predict))

                            # Tahminleri içeren veri setlerini oluştur
                            train_prediction_df = tesla_df.copy()
                            train_prediction_df.iloc[lookback:train_size, 0] = train_predict[:, 0]

                            test_prediction_df = tesla_df.copy()
                            test_prediction_df.iloc[train_size + lookback:, 0] = test_predict[:, 0]

                            # Tahminleri görselleştir
                            #plt.figure(figsize=(14, 5))
                            #plt.plot(tesla_df, label='Real Values')
                            #plt.plot(train_prediction_df, color='blue', label='Train Predicted')
                            #plt.plot(test_prediction_df, color='red', label='Test Predicted')
                            #plt.ylabel('Stock Values')
                            #plt.xlabel('Time')
                            #plt.legend()
                            #plt.show()

                            import pandas as pd
                            import numpy as np
                            from sklearn.preprocessing import MinMaxScaler
                            from tensorflow.keras.models import load_model
                            import os

                            # Eğittiğiniz modelin kaydedildiği h5 dosyasının adı
                            model_filename = filep

                            # Önceki verileri içeren dönem uzunluğu (lookback) ve tahmin edilecek dönem uzunluğu
                            # Önceki verileri içeren dönem uzunluğu (lookback) ve tahmin edilecek dönem uzunluğu
                            lookback = 4
                            prediction_period = 4

                            # Veri setini yükle
                            df = pd.read_csv(inputdf)

                            # Veri setini datetime formatına dönüştür
                            df['Date'] = pd.to_datetime(df['Date'])

                            # Kapanış fiyatlarını içeren sütunu seç
                            bitcoin_df = df[['Date', 'Close']]

                            # Tarih sütununu indeks olarak ayarla
                            bitcoin_df.set_index('Date', inplace=True)

                            # Veri setini ölçeklendir
                            scaler = MinMaxScaler(feature_range=(0, 1))
                            scaled_data = scaler.fit_transform(bitcoin_df)

                            # Modeli yükle
                            model = load_model(model_filename)

                            # En son veri setinin dönem uzunluğu kadarını al
                            recent_data = scaled_data[-lookback:]

                            # Veriyi yeniden şekillendir
                            recent_data = np.reshape(recent_data, (1, lookback, 1))

                            # Tahmin yap
                            predicted_price = model.predict(recent_data)

                            # Tahmini tersine çevirerek gerçek değere dönüştür
                            predicted_price = scaler.inverse_transform(predicted_price)[0][0]

                            print(f"Train RMSE: {train_rmse}")
                            print(f"Test RMSE: {test_rmse}")
                            model_success = (1 - train_rmse / 67549.14) * 100 , (1 - test_rmse / 67549.14) * 100
                            print(model_success)
                            loss = model.evaluate(X_test, y_test, batch_size=20)
                            print("\nTest loss: %.1f%%" % (100.0 * loss))
                            print("\n4 gün sonrasının tahmini fiyat:", predicted_price)
                            bekle(1)
                            os.remove(inputdf)
                            print("\n Sevgili kullanıcı, veri karışıklığını önlemek amacıyla oluşturduğunuz {} dosyası silinmiştir "+"lstm data yazarak tekrar oluşturabilirsiniz...".format(inputdf))

                
            elif "ip" in command or "ipconfig" in command or "ifconfig" in command:
                    host = socket.gethostname()
                    ip = socket.gethostbyname(host)
                    print("Wix: IP'niz: {}".format(ip))
                
            elif "şaka yap" in command or "şaka yaz" in command or "şaka" in command or "beni biraz güldür" in command or "bizi güldür" in command:
                            rando = random.randint(0,5)
                            saka = sakalar[rando]
                            output(saka)

            else:
                    print(command)
                    
        def exit_console():
            sys.exit()

        root = tk.Tk()
        root.title("Python Konsolu")
        root.attributes("-topmost", True)
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        input_text = tk.Text(input_frame, width=60, height=5)  # Yükseklik ayarı burada yapılıyor
        input_text.pack(side=tk.LEFT)

            #    execute_button = tk.Button(input_frame, text="Çalıştır", command=execute_command)
            #    execute_button.pack(side=tk.LEFT, padx=10)
        output_text = tk.Text(root, width=60, height=20)
        output_text.pack()

        exit_button = tk.Button(root, text="Çalıştır", command=execute_command)
        exit_button.pack(pady=10)

        # Çıktıyı yönlendir
        sys.stdout = RedirectedOutput(output_text)

        root.mainloop()


    def open_main_page():
        window2 = tk.Tk()
        window2.title("WixOS Arayüzü")

        # Pencere boyutu ve konumu
        screen_width = window2.winfo_screenwidth()
        screen_height = window2.winfo_screenheight()
        window2.geometry(f"{screen_width}x{screen_height}+1+1")

        # Pencereyi tam ekran yapma
        #window2.attributes("-fullscreen", True)

        def exit_program():
            def confirm_exit():
                if messagebox.askyesno("Çıkış", "Programdan çıkmak istediğinize emin misiniz?", parent=exit_window):
                    window2.destroy()  # Ana pencereyi kapat
                    sys.exit()  # Programı sonlandır

            exit_window = tk.Toplevel(window2)
            exit_window.title("Çıkış")
            exit_window.geometry("300x100")
            exit_window.resizable(False, False)
            exit_window.attributes("-topmost", True)  # Pencereyi en üste getir

            label_exit = tk.Label(exit_window, text="Programdan çıkmak istediğinize emin misiniz?")
            label_exit.pack(pady=10)

            button_yes = tk.Button(exit_window, text="Evet", command=confirm_exit)
            button_yes.pack( padx=10)

            button_no = tk.Button(exit_window, text="Hayır", command=exit_window.destroy)
            button_no.pack( padx=10)

            exit_window.mainloop()

            window2.deiconify()

        menu_bar = tk.Menu(window2)

        status_frame = tk.Frame(window2, relief="sunken")
        status_frame.place(relx=1.0, rely=1.012, anchor="se", x=-10, y=-10)

        datetime_label = tk.Label(status_frame, font=("Arial", 12))
        datetime_label.pack(side="left", padx=10, pady=5)

        battery_label = tk.Label(status_frame, font=("Arial", 12))
        battery_label.pack(side="left", padx=10, pady=5)

        wifi_label = tk.Label(status_frame, font=("Arial", 12))#, fg="white", bg="black")
        wifi_label.pack(side="left", padx=10, pady=5)

        frame_orta = tk.Frame(window2, bg="#808080")
        frame_orta.place(relx=0.0001, rely= 0.951, relwidth=7, relheight=0.009)

        def update_date_time():
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            datetime_label.config(text=f"Tarih: {current_date}   Saat: {current_time}")
            datetime_label.after(1000, update_date_time)

        def update_battery():
            battery_percent = psutil.sensors_battery()
            battery_label.config(text=f"Pil Gücü: {battery_percent}%")
            battery_label.after(60000, update_battery)

        

        update_date_time()
        update_battery()

        #uygulamalar...
        first_index = tk.Frame(window2, relief="sunken")
        first_index.place(relx=0.087, rely=0.03, anchor="center")
        second_index = tk.Frame(window2, relief="sunken")
        second_index.place(relx=0.07, rely=0.08, anchor="center")
        third_index = tk.Frame(window2, relief="sunken")
        third_index.place(relx=0.056, rely=0.13, anchor="center")

        button_system = tk.Button(first_index, text="System Infos", font=("Arial", 12), command=system_infos)
        button_system.pack(side="left", padx=10, pady=5)

        button_app1 = tk.Button(first_index, text="Python Console", font=("Arial", 12), command=python)
        button_app1.pack(side="left", padx=10, pady=10)

        wix_browser = tk.Button(second_index, text="Wix Browser", font=("Arial", 12), command=browser)
        wix_browser.pack(side="left", padx=10, pady=5)

        button_browser = tk.Button(second_index, text="Google", font=("Arial", 12), command=google)
        button_browser.pack(side="left", padx=10, pady=10)

        button_notepad = tk.Button(third_index, text="Notepad", font=("Arial", 12), command=notepad)
        button_notepad.pack(side="left", padx=10, pady=10)

        button_wix= tk.Button(third_index, text="Wix", font=("Arial", 12), command=wix)
        button_wix.pack(side="left", padx=10, pady=5)
        #...

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", font=("Arial", 12), command=exit_program)
        menu_bar.add_cascade(label="WixOS", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Yeni Dosya")
        help_menu.add_command(label="Dosya Aç")
        menu_bar.add_cascade(label="Dosya", menu=help_menu)

        app_menu = tk.Menu(menu_bar, tearoff=0)
        app_menu.add_command(label="Sistem Özellikleri", command=system_infos)
        app_menu.add_command(label="Python Console", command=python)
        app_menu.add_command(label="Wix Browser", command=browser)
        app_menu.add_command(label="Google", command=google)
        app_menu.add_command(label="Notepad", command=notepad)
        app_menu.add_command(label="Wix", command=wix)
        menu_bar.add_cascade(label="Uygulamalar", menu=app_menu)

        help_menu1 = tk.Menu(menu_bar, tearoff=0)
        help_menu1.add_command(label="Hakkında")
        menu_bar.add_cascade(label="Yardım", menu=help_menu1)

        window2.config(menu=menu_bar)

        window2["highlightbackground"] = "black"
        window2["highlightcolor"] = "black"

        window2.iconbitmap("cizgifikrim.icon")

        #window2.wm_attributes("-topmost", True)

        exit_button = tk.Button(window2, text="Çıkış", command=exit_program)
        exit_button.pack(side="left", padx=10, anchor="s")

        window2.mainloop()

    window = tk.Tk()
    window.title("Kullanıcı Girişi")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")
    window.attributes("-fullscreen", True)
    # Ana frame
    main_frame = tk.Frame(window)
    main_frame.pack(expand=True)

    # Kullanıcı girişi bölümü
    login_frame = tk.Frame(main_frame)
    login_frame.pack(side=tk.LEFT, padx=(screen_width//4, 0))

    label_username = tk.Label(login_frame, text="Kullanıcı Adı:")
    label_username.pack()
    entry_username = tk.Entry(login_frame)
    entry_username.pack()

    label_password = tk.Label(login_frame, text="Parola:")
    label_password.pack()
    entry_password = tk.Entry(login_frame, show="*")
    entry_password.pack()

    login_button = tk.Button(login_frame, text="Giriş Yap", command=login)
    login_button.pack(pady=20)

    # Fotoğraf bölümü
    image_frame = tk.Frame(main_frame)
    image_frame.pack(side=tk.RIGHT, padx=(0, screen_width//4))

    window.mainloop()
main()