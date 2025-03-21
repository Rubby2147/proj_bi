document.addEventListener("DOMContentLoaded",function (){
    const token = localStorage.getItem("token");
    if (token){
        mostrardashboard();
    }
})

function registrar(){
    const nome=document.getElementById("nome").value;
    const end = document.getElementById("end").value;
    const cidade= document.getElementById("cidade").value;
    const fone= document.getElementById("fone").value;
    const email = document.getElementById("email").value;
    
    fetch("http://localhost:5000/registro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, end, cidade, fone, email })
    })
    .then(res => res.json())
    .then(data => alert(data.mensagem))
    .catch(err => console.error(err));
}