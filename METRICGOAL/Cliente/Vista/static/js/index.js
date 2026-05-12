import { LoginController } from './loginController.js'

const loginController = new LoginController()

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm')
    const errorDisplay = document.getElementById('errorMessage')

    loginForm.addEventListener('submit', (e) => {
        e.preventDefault()
        const email = document.getElementById('email').value
        const password = document.getElementById('password').value
        loginController.login(email, password, errorDisplay)
    })
})