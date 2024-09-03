// Register Start
if (window.location.pathname.includes('register') || window.location.pathname.includes('password_reset')){
    document.querySelectorAll('#register-btn, #reset-pass-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            let email = document.getElementById('id_email');
            if (!email) {
                alert('Something went wrong!');
                window.location.href = '/';
                return;
            }
            if (!email.value) {
                return;
            }
            localStorage.setItem('email', email.value);
        });
    });
};
// Register End

// Account Activation Start
if (window.location.pathname.includes('activate-account')){
    const aaEmail = document.getElementById('aa_email');
    let email = localStorage.getItem('email');
    if (!aaEmail || !email){
        alert('something went wrong!');
        window.location.href = '/';
    };
    aaEmail.value = email;
};
// Account Activation End

// Logout Start
if (window.location.pathname.includes('profile')){
    document.getElementById('logout-user').addEventListener('click', (e)=>{
        window.location.href = '/logout';
    });
};
// Logout End

// Account Activation Start
if (window.location.pathname.includes('reset-password')){
    const emailEle = document.getElementById('email');
    let email = localStorage.getItem('email');
    if (!emailEle || !email){
        alert('something went wrong!');
        window.location.href = '/';
    };
    emailEle.value = email;
};
// Account Activation End

// Book-Detail Start
if (window.location.pathname.includes('book')){
    document.getElementById('submit-review').addEventListener('click', (e)=>{
        e.target.style.display = 'none';
        document.getElementById('review-form').hidden = false;
    });

    document.getElementById('cancle-review').addEventListener('click', (e)=>{
        document.getElementById('submit-review').style.display = 'unset';
        document.getElementById('review-form').hidden = true;
    });

    const stars = document.querySelectorAll('.review-ratings');
    stars.forEach((star, index) => {
        star.addEventListener('click', () => {
            const rating = parseInt(star.getAttribute('data-id'));
            stars.forEach((s, i) => {
                if (i <= rating) {
                    s.classList.add('y-rating');
                    s.classList.remove('no-rating');
                } else {
                    s.classList.remove('y-rating');
                    s.classList.add('no-rating');
                }
            });
            document.getElementById('rating').value = rating + 1;
        });
    });
};
// Book-Detail End
