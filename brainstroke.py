import streamlit as st
import pickle
import re
import numpy as np
from sklearn.linear_model import LogisticRegression
import time

st.set_page_config(page_title='پیش بینی سکته مغزی - RoboAi', layout='centered', page_icon='🧠')

def load_model():
    with open('saved.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

model = data['model']
x = data['x']

def show_page():
    st.write("<h3 style='text-align: center; color: blue;'>سامانه پیش بینی سکته مغزی 🧠</h3>", unsafe_allow_html=True)
    st.write("<h5 style='text-align: center; color: gray;'>Robo-Ai.ir طراحی شده توسط</h5>", unsafe_allow_html=True)
    st.link_button("Robo-Ai بازگشت به", "https://robo-ai.ir")
    with st.sidebar:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            st.image('img.png')
        with col3:
            st.write(' ')
        st.divider()
        st.write("<h4 style='text-align: center; color: black;'>پیش بینی بروز سکته مغزی در سالمندان</h4>", unsafe_allow_html=True)
        st.write("<h4 style='text-align: center; color: gray;'>بر اساس تحلیل سبک زندگی</h4>", unsafe_allow_html=True)
        st.divider()
        st.write("<h5 style='text-align: center; color: black;'>طراحی و توسعه</h5>", unsafe_allow_html=True)
        st.write("<h5 style='text-align: center; color: black;'>حمیدرضا بهرامی</h5>", unsafe_allow_html=True)


    container = st.container(border=True)
    container.write("<h6 style='text-align: right; color: gray;'>پرسشنامه پیش بینی احتمال بروز سکته مغزی 📋</h6>", unsafe_allow_html=True)
    container.write("<h6 style='text-align: right; color: gray;'>.برای افزایش دقت تحلیل سامانه ، توسط اطرافیان شخص سالمند پاسخ داده شود ⚠️</h6>", unsafe_allow_html=True)
        
    g = ('مرد' , 'زن')
    g = st.selectbox('جنسیت شما', g)
    if g == 'مرد':
        gender = 1.0
    else:
        gender = 0.0

    age = st.slider('سن شما', 10.0, 100.0, 35.0)

    h = ('بله' , 'خیر')
    h = st.selectbox('آیا فشار خون دارید؟', h)
    if h == 'بله':
        hypertension = 1.0
    else:
        hypertension = 0.0

    hd = ('بله' , 'خیر')
    hd = st.selectbox('آیا بیماری قلبی یا سابقه سکته قلبی دارید؟', hd)
    if hd == 'بله':
        heart_disease = 1.0
    else:
        heart_disease = 0.0

    m = ('بله' , 'خیر')
    m = st.selectbox('آیا تاکنون ازدواج کرده اید؟ - وضعیت تاهل در حال حاضر مدنظر نیست', m)
    if m == 'بله':
        ever_married = 1.0
    else:
        ever_married = 0.0

    wt = ('کسب و کار شخصی دارم / داشتم' , 'شغل دولتی دارم / داشتم', 'هیچ شغلی ندارم / نداشتم', 'فرزندانم خرج را می دهند')
    wt = st.selectbox('وضعیت یا سابقه شغلی خود را مشخص کنید', wt)
    if wt == 'کسب و کار شخصی دارم / داشتم':
        work_type = 1.0
    elif wt == 'شغل دولتی دارم / داشتم':
        work_type = 0.0
    elif wt == 'هیچ شغلی ندارم / نداشتم':
        work_type = 3.0
    else:
        work_type = 2.0
    
    rt = ('شهر' , 'روستا')
    rt = st.selectbox('بیشتر عمر خود شما در کجا سپری شده است؟', rt)
    if rt == 'بله':
        Residence_type = 1.0
    else:
        Residence_type = 0.0

    avg_glucose_level = st.slider('گلوگز خون شما بطور میانگین روی چه عددی است؟', 55.0, 270.0, 75.0)

    bmi = st.slider('شاخص توده بدنی خود را مشخص کنید', 11.0, 92.0, 25.0)

    smt = ('هرگز سیگار / قلیان نکشیده ام' , 'قبلا سیگار / قلیان می کشیدم', 'الان سیگار / قلیان می کشم')
    smt = st.selectbox('وضعیت استعمال دخانیات خود را مشخص کنید', smt)
    if smt == 'هرگز سیگار / قلیان نکشیده ام':
        smoking_status = 0.0
    elif st == 'قبلا سیگار / قلیان می کشیدم':
        smoking_status = 1.0
    else:
        smoking_status = 2.0
    
    button = st.button('پیش بینی')
    if button:
        with st.chat_message("assistant"):
                with st.spinner('''درحال بررسی لطفا صبور باشید'''):
                    time.sleep(2)
                    st.success(u'\u2713''تحلیل انجام شد')
                    x = np.array([[gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level,
                                   bmi, smoking_status]])
        x = x.astype(float)

        y = model.predict(x)
        if y == 1:
            text1 = 'بر اساس تحلیل من ، احتمال بروز سکته مغزی در شما یا کاربر موردنظر بالا است'
            text2 = 'ادامه ی روند زندگی به شکل بالا ، موجب افزایش ریسک سکته مغزی در شما یا شخص سالمند موردنظر خواهد شد'
            text3 = 'لطفا در اسرع وقت به پزشک مراجعه کنید'
            text4 = 'Based on my analysis, you have a high chance of having Brain Stoke , if you or the user you mentioned continue to live like this'
            text5 = 'Please visit doctor as soon as possible'
            def stream_data1():
                for word in text1.split(" "):
                    yield word + " "
                    time.sleep(0.09)
            st.write_stream(stream_data1)
            def stream_data2():
                for word in text2.split(" "):
                    yield word + " "
                    time.sleep(0.09)
            st.write_stream(stream_data2)
            def stream_data3():
                for word in text3.split(" "):
                    yield word + " "
                    time.sleep(0.09)
            st.write_stream(stream_data3)
            def stream_data4():
                for word in text4.split(" "):
                    yield word + " "
                    time.sleep(0.09)
            st.write_stream(stream_data4)

        elif y == 0:
            text1 = 'بر اساس تحلیل من ، احتمال بروز سکته مغزی در شما یا کاربر موردنظر کم است'
            text2 = 'ادامه ی روند زندگی به شکل بالا ، موجب افزایش ریسک سکته مغزی در شما یا شخص سالمند موردنظر نخواهد شد'
            text3 = 'Based on my analysis, you have a low chance of having Brain Stoke , if you or the user you mentioned continue to live like this'
            def stream_data1():
                for word in text1.split(" "):
                    yield word + " "
                    time.sleep(0.09)
            st.write_stream(stream_data1)
            def stream_data2():
                for word in text2.split(" "):
                    yield word + " "
                    time.sleep(0.09)
            st.write_stream(stream_data2)
            def stream_data3():
                for word in text3.split(" "):
                    yield word + " "
                    time.sleep(0.09)
            st.write_stream(stream_data3)


show_page()
