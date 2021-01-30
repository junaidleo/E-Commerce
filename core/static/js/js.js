function home() {
    document.getElementById('home_content').hidden=false;
    document.getElementById('about_content').hidden=true;
    document.getElementById('contact_content').hidden=true;
}
function about() {
    document.getElementById('home_content').hidden=true;
    document.getElementById('about_content').hidden=false;
    document.getElementById('contact_content').hidden=true;
}
function contact() {
    document.getElementById('home_content').hidden=true;
    document.getElementById('about_content').hidden=true;
    document.getElementById('contact_content').hidden=false;
}