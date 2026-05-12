export function createUser(data) {
    return {
        nombre: data.nombre,
        club: data.club,
        equipo: data.equipo,
        idEquipo: data.id_equipo
    }
}