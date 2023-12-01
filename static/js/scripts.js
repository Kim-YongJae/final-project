window.addEventListener('DOMContentLoaded', (event) => {

    const sidebarToggle = document.body.querySelector('#sidebarToggle');

    if (sidebarToggle) {
        // 세션 스토리지에서 상태를 가져와서 처음 접속될 때만 사이드바를 숨김
        const isSidebarToggled = sessionStorage.getItem('sb|sidebar-toggle') !== 'false';
        document.body.classList.toggle('sb-sidenav-toggled', isSidebarToggled);

        sidebarToggle.addEventListener('click', (event) => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            sessionStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled').toString());
        });
    }
});
