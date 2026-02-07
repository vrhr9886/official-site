
let time = 30;
let timerInterval;

/* MESSAGE */
function showMessage(text, type){
  const box = msgBox;
  box.innerText = text;
  box.className = "msg " + type;
  box.style.display = "block";
  setTimeout(()=> box.style.display="none",3000);
}

function togglePassword(){
  password.type = password.type==="password" ? "text" : "password";
}

/* LOGIN */
function login(){
  fetch("/login",{
    method:"POST",
    headers:{"Content-Type":"application/x-www-form-urlencoded"},
    body:`username=${username.value}&password=${password.value}`
  })
  .then(r=>r.json())
  .then(d=>{
    if(d.status==="otp_sent"){
      showMessage("OTP sent to your mail","success");
      otpBox.style.display="block";
      btn.style.display="none";

      otpBtn.innerText = "Login";
      otpBtn.onclick = verifyOtp;

      resetTimer();
    }else{
      showMessage("Invalid credentials","error");
    }
  });
}

/* TIMER */
function resetTimer(){
  clearInterval(timerInterval);
  time = 30;
  startTimer();
}

function startTimer(){
  timerInterval = setInterval(()=>{
    timer.innerText = `OTP expires in 00:${time<10?'0'+time:time}`;
    time--;

    if(time < 0){
      clearInterval(timerInterval);

      // ❌ no message
      // ✅ Login → Resend OTP
      otpBtn.innerText = "Resend OTP";
      otpBtn.onclick = resendOtp;
    }
  },1000);
}

/* VERIFY OTP */
function verifyOtp(){
  fetch("/verify-otp",{
    method:"POST",
    headers:{"Content-Type":"application/x-www-form-urlencoded"},
    body:`otp=${otp.value}`
  })
  .then(r=>r.json())
  .then(d=>{
    if(d.status==="success"){
      loginBox.style.display="none";
      successPopup.style.display="flex";
      setTimeout(()=>window.location="/dashboard",1000);
    }
    else if(d.status==="expired"){
      otpBtn.innerText = "Resend OTP";
      otpBtn.onclick = resendOtp;
    }
    else{
      showMessage("Invalid OTP","error");
    }
  });
}

/* 🔁 RESEND OTP (same button) */
function resendOtp(){
  showMessage("Resending OTP...","success");

  fetch("/resend-otp",{method:"POST"})
  .then(r=>r.json())
  .then(d=>{
    if(d.status==="otp_sent"){
      showMessage("OTP resent to your mail","success");

      otpBtn.innerText = "Login";
      otpBtn.onclick = verifyOtp;

      resetTimer();
    }else{
      showMessage("Failed to resend OTP","error");
    }
  });
}

