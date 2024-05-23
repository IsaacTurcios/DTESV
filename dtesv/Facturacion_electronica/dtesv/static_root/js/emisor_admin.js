document.addEventListener('DOMContentLoaded', function() {
    const departamentoSelect = document.querySelector('select[name="departamento"]');
    const municipioSelect = document.querySelector('select[name="municipio"]');

    if (departamentoSelect && municipioSelect) {
        departamentoSelect.addEventListener('change', function() {
            const departamentoId = this.value;
            municipioSelect.innerHTML = '<option value="">---------</option>';  // Reset municipio options

            if (departamentoId) {
                const url =`/dtesv/admin/get_municipios_by_departamento/${departamentoId}/`;
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        for (const [id, name] of Object.entries(data)) {
                            const option = new Option(name, id);
                            municipioSelect.appendChild(option);
                        }
                    });
            }
        });

        // Load municipios if a departamento is already selected (edit case)
        if (departamentoSelect.value) {
            const departamentoId = departamentoSelect.value;
            const selectedMunicipioId = municipioSelect.dataset.selected;
            const url =`/dtesv/admin/get_municipios_by_departamento/${departamentoId}/`;

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    for (const [id, name] of Object.entries(data)) {
                        const option = new Option(name, id, id === selectedMunicipioId, id === selectedMunicipioId);
                        municipioSelect.appendChild(option);
                    }
                });
        }
    }
});
