import { createUser } from './userModel.js'

export class LoginController {
    async login(email, password, errorDisplay) {
        try {
            const response = await fetch('/login', {  // Ruta relativa, más limpio
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            })

            const result = await response.json()

            if (!response.ok) {
                errorDisplay.textContent = result.detail || "Credenciales incorrectas"
                errorDisplay.style.display = 'block'
                return
            }

            const user = createUser(result)
            localStorage.setItem('usuarioNombre', user.nombre)
            localStorage.setItem('usuarioClub', user.club)
            localStorage.setItem('usuarioEquipo', user.equipo)
            localStorage.setItem('idEquipo', user.idEquipo)

            window.location.href = '/dashboard'
        } catch (error) {
            errorDisplay.textContent = "🔌 Error: El servidor no responde."
            errorDisplay.style.display = 'block'
        }
    }
}