$(document).ready(function () {
    const searchForm = $(".search-form");
    const searchInput = searchForm.find("[name='q']"); // input name='q'
    let typingTimer;
    const typingInterval = 500; // 0.5 segundos
    const searchBtn = searchForm.find("[type='submit']");
  
    searchInput.keyup(function () {
      // Tecla liberada
      clearTimeout(typingTimer);
      typingTimer = setTimeout(performSearch, typingInterval);
    });
  
    searchInput.keydown(function () {
      // Tecla pressionada
      clearTimeout(typingTimer);
    });
  
    function displaySearching() {
      searchBtn.addClass("disabled");
      searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...");
    }
  
    function performSearch() {
      displaySearching();
      const query = searchInput.val();
      setTimeout(function () {
        window.location.href = "/search/?q=" + query;
      }, 1000);
    }
  });
  