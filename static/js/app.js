document.addEventListener('DOMContentLoaded', () => {
    // Step 22 Performance Optimization Helpers: RAF & Debounce Controllers
    function debounce(func, delay = 120) {
        let timer;
        return function (...args) {
            clearTimeout(timer);
            timer = setTimeout(() => func.apply(this, args), delay);
        };
    }

    function requestAnimationFrameThrottle(func) {
        let ticking = false;
        return function (...args) {
            if (!ticking) {
                requestAnimationFrame(() => {
                    func.apply(this, args);
                    ticking = false;
                });
                ticking = true;
            }
        };
    }

    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    const dropzonePrompt = document.getElementById('dropzone-prompt');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeImgBtn = document.getElementById('remove-img-btn');

    // Preset Samples Grid Container
    const presetSamplesGrid = document.getElementById('preset-samples-grid');

    // Region Sampler Controls & Canvas
    const toggleRegionBtn = document.getElementById('toggle-region-btn');
    const clearRegionBtn = document.getElementById('clear-region-btn');
    const regionStatus = document.getElementById('region-status');
    const regionCanvas = document.getElementById('region-canvas');
    const ctx = regionCanvas ? regionCanvas.getContext('2d') : null;

    // Extraction Controls & Output
    const algorithmSelect = document.getElementById('algorithm-select');
    const colorCountSlider = document.getElementById('color-count-slider');
    const colorCountVal = document.getElementById('color-count-val');
    const perceptualFilterCheckbox = document.getElementById('perceptual-filter-checkbox');
    const extractBtn = document.getElementById('extract-btn');
    const paletteSection = document.getElementById('palette-section');
    const paletteGrid = document.getElementById('palette-grid');

    // Studio Tabs & Panels
    const studioTabs = document.querySelectorAll('.studio-tab');
    const tabPanes = document.querySelectorAll('.tab-pane');

    // Step 18: CIEDE2000 Matcher Controls & Containers
    const ciedeLibrarySelect = document.getElementById('ciede-library-select');
    const ciedeCustomTargetInput = document.getElementById('ciede-custom-target-input');
    const ciedeRunCustomBtn = document.getElementById('ciede-run-custom-btn');
    const ciedeMatchesGrid = document.getElementById('ciede-matches-grid');
    const ciedeAvgDistVal = document.getElementById('ciede-avg-dist-val');
    const ciedeMatrixTable = document.getElementById('ciede-matrix-table');

    // Step 19 & 22: Real-Time Image Recolor & Palette Swap Simulator Controls
    const recolorMappingGrid = document.getElementById('recolor-mapping-grid');
    const recolorToleranceSlider = document.getElementById('recolor-tolerance-slider');
    const recolorToleranceVal = document.getElementById('recolor-tolerance-val');
    const recolorPreserveLuminance = document.getElementById('recolor-preserve-luminance');
    const applyRecolorBtn = document.getElementById('apply-recolor-btn');
    const resetRecolorBtn = document.getElementById('reset-recolor-btn');
    const downloadRecoloredBtn = document.getElementById('download-recolored-btn');
    const recolorResultCanvas = document.getElementById('recolor-result-canvas');
    let recolorTargetMappings = [];

    // Spatial Coverage Elements
    const spatialSummaryBar = document.getElementById('spatial-summary-bar');
    const spatialCardsGrid = document.getElementById('spatial-cards-grid');

    // Gradient Studio Elements
    const gradientTypeSelect = document.getElementById('gradient-type-select');
    const gradientAngleGroup = document.getElementById('gradient-angle-group');
    const gradientAngleSlider = document.getElementById('gradient-angle-slider');
    const gradientAngleVal = document.getElementById('gradient-angle-val');
    const copyGradientCssBtn = document.getElementById('copy-gradient-css-btn');
    const gradientPreviewBox = document.getElementById('gradient-preview-box');
    let currentGradientCss = '';

    // CVD & WCAG Containers
    const cvdSelect = document.getElementById('cvd-select');
    const cvdPreviewGrid = document.getElementById('cvd-preview-grid');
    const wcagMatrixGrid = document.getElementById('wcag-matrix-grid');

    // Harmonies Studio Controls
    const harmonySwatchSelect = document.getElementById('harmony-swatch-select');
    const harmoniesContainer = document.getElementById('harmonies-container');

    // UI Mockup Frame Controls
    const uiMockupFrame = document.getElementById('ui-mockup-frame');
    const roleSelects = {
        primary: document.getElementById('role-primary'),
        surface: document.getElementById('role-surface'),
        accent: document.getElementById('role-accent'),
        bg: document.getElementById('role-bg'),
        text: document.getElementById('role-text')
    };

    // Palette Character & Analytics Dashboard Elements
    const analyticsProfileTitle = document.getElementById('analytics-profile-title');
    const analyticsProfileDesc = document.getElementById('analytics-profile-desc');
    const metricDomHue = document.getElementById('metric-dom-hue');
    const metricAvgSat = document.getElementById('metric-avg-sat');
    const metricAvgLight = document.getElementById('metric-avg-light');
    const metricLightRange = document.getElementById('metric-light-range');
    const hueDistributionBars = document.getElementById('hue-distribution-bars');

    // Code & Design Tokens Exporters
    const exportAseBtn = document.getElementById('export-ase-btn');
    const exportSvgBtn = document.getElementById('export-svg-btn');
    const codeTabs = document.querySelectorAll('.code-tab');
    const codeOutputBlock = document.getElementById('code-output-block');
    const copyCodeBtn = document.getElementById('copy-code-btn');
    let activeCodeFormat = 'tailwind';
    let generatedCodeSnippets = {};

    // Palette History Manager Controls
    const addSwatchBtn = document.getElementById('add-swatch-btn');
    const savePaletteBtn = document.getElementById('save-palette-btn');
    const historyFilterSelect = document.getElementById('history-filter-select');
    const clearHistoryBtn = document.getElementById('clear-history-btn');
    const historyGrid = document.getElementById('history-grid');

    // Action & Download Buttons
    const copyHexListBtn = document.getElementById('copy-hex-list-btn');
    const downloadPngBtn = document.getElementById('download-png-btn');
    const downloadCssBtn = document.getElementById('download-css-btn');
    const downloadJsonBtn = document.getElementById('download-json-btn');
    const regenerateUnlockedBtn = document.getElementById('regenerate-unlocked-btn');

    // Toast Container
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    let toastTimeout = null;

    let currentFile = null;
    let isRegionModeActive = false;
    let isDrawing = false;
    let startX = 0, startY = 0;
    let selectedRegion = null;
    let currentPalette = [];
    let currentPaletteId = null;

    if (colorCountSlider) {
        colorCountSlider.addEventListener('input', (e) => {
            if (colorCountVal) colorCountVal.innerText = e.target.value;
        });
    }

    loadPresetSamples();
    renderHistoryGrid();

    // Studio Tab Switching
    studioTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            studioTabs.forEach(t => t.classList.remove('active'));
            tabPanes.forEach(p => p.classList.add('hidden'));

            tab.classList.add('active');
            const target = document.getElementById(tab.getAttribute('data-target'));
            if (target) {
                target.classList.remove('hidden');
                if (tab.getAttribute('data-target') === 'tab-history') {
                    renderHistoryGrid();
                } else if (tab.getAttribute('data-target') === 'tab-recolor') {
                    renderRecolorMappingUI();
                    processImageRecolorThrottled();
                }
            }
        });
    });

    // Trigger File Input via Browse Button or Dropzone click
    if (browseBtn) {
        browseBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (fileInput) fileInput.click();
        });
    }

    if (dropzone) {
        dropzone.addEventListener('click', (e) => {
            if (!currentFile && e.target !== browseBtn && fileInput) fileInput.click();
        });

        // Drag & Drop Event Listeners
        ['dragenter', 'dragover'].forEach(eventName => {
            dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropzone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropzone.classList.remove('dragover');
            }, false);
        });

        dropzone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const file = dt ? dt.files[0] : null;
            if (file) handleFile(file);
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) handleFile(file);
        });
    }

    // Clipboard Paste Listener
    document.addEventListener('paste', (e) => {
        const items = (e.clipboardData || e.originalEvent?.clipboardData)?.items || [];
        for (let item of items) {
            if (item.type.indexOf('image') !== -1) {
                const blob = item.getAsFile();
                if (blob) handleFile(blob);
                break;
            }
        }
    });

    function handleFile(file) {
        const validTypes = ['image/png', 'image/jpeg', 'image/webp', 'image/svg+xml'];
        if (!validTypes.includes(file.type)) {
            alert('Please upload a valid image file (PNG, JPG, WebP, or SVG).');
            return;
        }

        if (file.size > 16 * 1024 * 1024) {
            alert('File size exceeds the 16MB limit.');
            return;
        }

        currentFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.onload = () => {
                resetRegionSelection();
                dropzonePrompt.classList.add('hidden');
                previewContainer.classList.remove('hidden');
                syncCanvasDimensions();
            };
        };
        reader.readAsDataURL(file);
    }

    if (removeImgBtn) {
        removeImgBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            currentFile = null;
            if (fileInput) fileInput.value = '';
            imagePreview.src = '';
            previewContainer.classList.add('hidden');
            dropzonePrompt.classList.remove('hidden');
            paletteSection.classList.add('hidden');
            paletteGrid.innerHTML = '';
            currentPalette = [];
            resetRegionSelection();
        });
    }

    // Load and Render Preset Samples Gallery
    async function loadPresetSamples() {
        if (!presetSamplesGrid) return;
        try {
            const res = await fetch('/api/samples');
            const data = await res.json();
            if (data.success) {
                presetSamplesGrid.innerHTML = '';
                data.samples.forEach(sample => {
                    const chip = document.createElement('button');
                    chip.type = 'button';
                    chip.className = 'preset-chip';
                    chip.innerHTML = `${sample.svg} <span>${sample.name}</span>`;
                    chip.addEventListener('click', (e) => {
                        e.stopPropagation();
                        loadPresetImage(sample);
                    });
                    presetSamplesGrid.appendChild(chip);
                });
            }
        } catch (err) {
            console.error('Failed to load sample presets:', err);
        }
    }

    function loadPresetImage(sample) {
        const svgBlob = new Blob([sample.svg], { type: 'image/svg+xml' });
        const file = new File([svgBlob], `${sample.id}.svg`, { type: 'image/svg+xml' });
        handleFile(file);
    }

    // Interactive Region Sampler Logic
    function syncCanvasDimensions() {
        if (!regionCanvas || !imagePreview.complete || imagePreview.naturalWidth === 0) return;
        regionCanvas.width = imagePreview.clientWidth;
        regionCanvas.height = imagePreview.clientHeight;
        redrawCanvasOverlay();
    }

    window.addEventListener('resize', debounce(syncCanvasDimensions, 100));

    if (toggleRegionBtn) {
        toggleRegionBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            isRegionModeActive = !isRegionModeActive;
            if (isRegionModeActive) {
                toggleRegionBtn.classList.add('active');
                if (regionCanvas) regionCanvas.classList.remove('hidden');
                syncCanvasDimensions();
                if (regionStatus) regionStatus.innerText = selectedRegion ? 'Target: Custom Region' : 'Target: Drag on image to select region';
            } else {
                toggleRegionBtn.classList.remove('active');
                if (!selectedRegion && regionCanvas) {
                    regionCanvas.classList.add('hidden');
                }
                if (regionStatus) regionStatus.innerText = selectedRegion ? 'Target: Custom Region' : 'Target: Full Image';
            }
        });
    }

    if (clearRegionBtn) {
        clearRegionBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            resetRegionSelection();
        });
    }

    function resetRegionSelection() {
        selectedRegion = null;
        isDrawing = false;
        if (clearRegionBtn) clearRegionBtn.classList.add('hidden');
        if (regionStatus) regionStatus.innerText = 'Target: Full Image';
        if (ctx && regionCanvas) ctx.clearRect(0, 0, regionCanvas.width, regionCanvas.height);
        if (!isRegionModeActive && regionCanvas) {
            regionCanvas.classList.add('hidden');
        }
    }

    function getCanvasCoordinates(e) {
        if (!regionCanvas) return { x: 0, y: 0 };
        const rect = regionCanvas.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        return {
            x: Math.max(0, Math.min(rect.width, clientX - rect.left)),
            y: Math.max(0, Math.min(rect.height, clientY - rect.top))
        };
    }

    function startDrawing(e) {
        if (!isRegionModeActive) return;
        e.preventDefault();
        isDrawing = true;
        const coords = getCanvasCoordinates(e);
        startX = coords.x;
        startY = coords.y;
    }

    function draw(e) {
        if (!isDrawing || !isRegionModeActive || !regionCanvas) return;
        e.preventDefault();
        const coords = getCanvasCoordinates(e);
        const currentX = coords.x;
        const currentY = coords.y;

        const x = Math.min(startX, currentX);
        const y = Math.min(startY, currentY);
        const width = Math.abs(currentX - startX);
        const height = Math.abs(currentY - startY);

        selectedRegion = {
            x: x / regionCanvas.width,
            y: y / regionCanvas.height,
            width: width / regionCanvas.width,
            height: height / regionCanvas.height
        };

        redrawCanvasOverlay();
    }

    function stopDrawing() {
        if (!isDrawing) return;
        isDrawing = false;
        if (selectedRegion && (selectedRegion.width < 0.02 || selectedRegion.height < 0.02)) {
            selectedRegion = null;
            redrawCanvasOverlay();
            if (regionStatus) regionStatus.innerText = 'Target: Drag on image to select region';
            if (clearRegionBtn) clearRegionBtn.classList.add('hidden');
        } else if (selectedRegion) {
            if (clearRegionBtn) clearRegionBtn.classList.remove('hidden');
            if (regionStatus) regionStatus.innerText = 'Target: Custom Region Active';
        }
    }

    function redrawCanvasOverlay() {
        if (!ctx || !regionCanvas) return;
        ctx.clearRect(0, 0, regionCanvas.width, regionCanvas.height);
        if (!selectedRegion) return;

        const rx = selectedRegion.x * regionCanvas.width;
        const ry = selectedRegion.y * regionCanvas.height;
        const rw = selectedRegion.width * regionCanvas.width;
        const rh = selectedRegion.height * regionCanvas.height;

        ctx.fillStyle = 'rgba(15, 23, 42, 0.55)';
        ctx.fillRect(0, 0, regionCanvas.width, regionCanvas.height);
        ctx.clearRect(rx, ry, rw, rh);

        ctx.strokeStyle = '#8b5cf6';
        ctx.lineWidth = 2;
        ctx.setLineDash([6, 4]);
        ctx.strokeRect(rx, ry, rw, rh);
    }

    if (regionCanvas) {
        regionCanvas.addEventListener('mousedown', startDrawing);
        regionCanvas.addEventListener('mousemove', draw);
        window.addEventListener('mouseup', stopDrawing);

        regionCanvas.addEventListener('touchstart', startDrawing);
        regionCanvas.addEventListener('touchmove', draw);
        window.addEventListener('touchend', stopDrawing);
    }

    // Backend Extraction API Integration
    async function triggerExtraction(preserveLocks = false) {
        if (!currentFile) {
            alert('Please upload an image or select a sample preset first.');
            return;
        }

        const formData = new FormData();
        formData.append('image', currentFile);
        formData.append('color_count', colorCountSlider ? colorCountSlider.value : 5);
        formData.append('algorithm', algorithmSelect ? algorithmSelect.value : 'kmeans');
        formData.append('perceptual_filter', (perceptualFilterCheckbox && perceptualFilterCheckbox.checked) ? 'true' : 'false');
        if (selectedRegion) {
            formData.append('region', JSON.stringify(selectedRegion));
        }

        if (preserveLocks && currentPalette.length > 0) {
            const lockedList = [];
            currentPalette.forEach((c, index) => {
                if (c.is_locked) {
                    lockedList.push({
                        index: index,
                        hex: c.hex,
                        rgb_values: c.rgb_values
                    });
                }
            });
            if (lockedList.length > 0) {
                formData.append('locked_colors', JSON.stringify(lockedList));
            }
        }

        if (extractBtn) {
            extractBtn.disabled = true;
            extractBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Extracting...';
        }
        if (regenerateUnlockedBtn) regenerateUnlockedBtn.disabled = true;

        try {
            const response = await fetch('/api/extract', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (data.success) {
                currentPalette = data.palette;
                currentPaletteId = 'pal_' + Date.now();
                renderPalette(currentPalette);
                updateStudioViews();
                autoSaveToHistory(currentPalette);

                if (data.analytics) {
                    renderAnalytics(data.analytics);
                }
                if (data.spatial_distribution) {
                    renderSpatialDistribution(data.spatial_distribution);
                }
            } else {
                alert('Extraction failed: ' + (data.error || 'Unknown error'));
            }
        } catch (err) {
            alert('Server request failed. Check server logs.');
        } finally {
            if (extractBtn) {
                extractBtn.disabled = false;
                extractBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Extract Palette';
            }
            if (regenerateUnlockedBtn) regenerateUnlockedBtn.disabled = false;
        }
    }

    if (extractBtn) {
        extractBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            triggerExtraction(false);
        });
    }

    if (regenerateUnlockedBtn) {
        regenerateUnlockedBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            triggerExtraction(true);
        });
    }

    // Render Swatch Cards with Color Name Badges
    function renderPalette(palette) {
        if (!paletteGrid) return;
        paletteGrid.innerHTML = '';
        let hasAnyLocked = false;

        palette.forEach((color, index) => {
            if (color.is_locked) hasAnyLocked = true;

            const card = document.createElement('div');
            card.className = `swatch-card ${color.is_locked ? 'is-locked' : ''}`;
            card.innerHTML = `
                <div class="swatch-card-header-actions">
                    <button type="button" class="btn-swatch-action btn-lock ${color.is_locked ? 'locked' : ''}" title="${color.is_locked ? 'Unlock Color' : 'Lock Color'}">
                        <i class="fa-solid ${color.is_locked ? 'fa-lock' : 'fa-lock-open'}"></i>
                    </button>
                    <button type="button" class="btn-swatch-action btn-delete" title="Delete Swatch">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                </div>

                <div class="swatch-box" style="background-color: ${color.hex}">
                    <div class="swatch-overlay">Click to Copy HEX</div>
                </div>

                <div class="swatch-info">
                    <span class="swatch-name-tag" title="${color.name || 'Custom Swatch'}">${color.name || 'Custom Swatch'}</span>
                    <div class="hex-editor-wrapper">
                        <input type="color" class="native-color-input" value="${color.hex}">
                        <input type="text" class="hex-text-input" value="${color.hex.toUpperCase()}" maxlength="7">
                    </div>
                    <div class="copy-badge" data-copy="${color.rgb}">
                        <span class="label">RGB</span>
                        <span class="val">${color.rgb_values ? color.rgb_values.join(', ') : color.rgb}</span>
                    </div>
                    <div class="copy-badge" data-copy="${color.hsl}">
                        <span class="label">HSL</span>
                        <span class="val">${color.hsl_values ? `${color.hsl_values.h}°, ${color.hsl_values.s}%, ${color.hsl_values.l}%` : color.hsl}</span>
                    </div>
                </div>

                <div class="swatch-reorder-bar">
                    <button type="button" class="btn-move-swatch btn-move-left" ${index === 0 ? 'disabled style="opacity:0.3;"' : ''}>
                        <i class="fa-solid fa-chevron-left"></i>
                    </button>
                    <span style="font-size: 0.7rem; color: var(--text-muted); font-weight: 600;">#${index + 1}</span>
                    <button type="button" class="btn-move-swatch btn-move-right" ${index === palette.length - 1 ? 'disabled style="opacity:0.3;"' : ''}>
                        <i class="fa-solid fa-chevron-right"></i>
                    </button>
                </div>
            `;

            // Lock Action
            const lockBtn = card.querySelector('.btn-lock');
            lockBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                color.is_locked = !color.is_locked;
                renderPalette(currentPalette);
            });

            // Delete Action
            const delBtn = card.querySelector('.btn-delete');
            delBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                if (currentPalette.length <= 2) {
                    alert('A palette must have at least 2 swatches.');
                    return;
                }
                currentPalette.splice(index, 1);
                renderPalette(currentPalette);
                updateStudioViews();
                autoSaveToHistory(currentPalette);
            });

            // Swatch Box Click Copy
            const swatchBox = card.querySelector('.swatch-box');
            swatchBox.addEventListener('click', () => copyToClipboard(color.hex, `HEX ${color.hex}`));

            // Dynamic Color Editing Trigger
            const colorPicker = card.querySelector('.native-color-input');
            const hexTextInput = card.querySelector('.hex-text-input');

            colorPicker.addEventListener('input', (e) => {
                updateColorValue(index, e.target.value);
            });

            hexTextInput.addEventListener('change', (e) => {
                let val = e.target.value.trim();
                if (!val.startsWith('#')) val = '#' + val;
                if (/^#([A-Fa-f0-9]{6})$/.test(val)) {
                    updateColorValue(index, val);
                } else {
                    e.target.value = color.hex.toUpperCase();
                }
            });

            // Reordering Controls
            const moveLeftBtn = card.querySelector('.btn-move-left');
            const moveRightBtn = card.querySelector('.btn-move-right');

            moveLeftBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                if (index > 0) {
                    const temp = currentPalette[index];
                    currentPalette[index] = currentPalette[index - 1];
                    currentPalette[index - 1] = temp;
                    renderPalette(currentPalette);
                    updateStudioViews();
                }
            });

            moveRightBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                if (index < currentPalette.length - 1) {
                    const temp = currentPalette[index];
                    currentPalette[index] = currentPalette[index + 1];
                    currentPalette[index + 1] = temp;
                    renderPalette(currentPalette);
                    updateStudioViews();
                }
            });

            card.querySelectorAll('.copy-badge').forEach(badge => {
                badge.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const textToCopy = badge.getAttribute('data-copy');
                    const label = badge.querySelector('.label').innerText;
                    copyToClipboard(textToCopy, `${label}: ${textToCopy}`);
                });
            });

            paletteGrid.appendChild(card);
        });

        if (regenerateUnlockedBtn) {
            if (hasAnyLocked) {
                regenerateUnlockedBtn.classList.remove('hidden');
            } else {
                regenerateUnlockedBtn.classList.add('hidden');
            }
        }

        if (paletteSection) paletteSection.classList.remove('hidden');
    }

    // Helper to Update Swatch Values & Dynamically Fetch Color Name
    async function updateColorValue(index, newHex) {
        const hex = newHex.toLowerCase();
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);

        // Calculate HSL
        const rNorm = r / 255, gNorm = g / 255, bNorm = b / 255;
        const max = Math.max(rNorm, gNorm, bNorm), min = Math.min(rNorm, gNorm, bNorm);
        let h = 0, s = 0, l = (max + min) / 2;

        if (max !== min) {
            const d = max - min;
            s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
            switch (max) {
                case rNorm: h = (gNorm - bNorm) / d + (gNorm < bNorm ? 6 : 0); break;
                case gNorm: h = (bNorm - rNorm) / d + 2; break;
                case bNorm: h = (rNorm - gNorm) / d + 4; break;
            }
            h /= 6;
        }

        const hslH = Math.round(h * 360);
        const hslS = Math.round(s * 100);
        const hslL = Math.round(l * 100);

        currentPalette[index].hex = hex;
        currentPalette[index].rgb = `rgb(${r}, ${g}, ${b})`;
        currentPalette[index].rgb_values = [r, g, b];
        currentPalette[index].hsl = `hsl(${hslH}, ${hslS}%, ${hslL}%)`;
        currentPalette[index].hsl_values = { h: hslH, s: hslS, l: hslL };

        // Fetch matched color name from server
        try {
            const nameRes = await fetch('/api/name', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ rgb_values: [r, g, b], hex: hex })
            });
            const nameData = await nameRes.json();
            if (nameData.success) {
                currentPalette[index].name = nameData.name;
            }
        } catch (e) {
            console.error('Failed to name color:', e);
        }

        renderPalette(currentPalette);
        updateStudioViews();
        autoSaveToHistory(currentPalette);
    }

    // Add Custom Swatch Handler
    if (addSwatchBtn) {
        addSwatchBtn.addEventListener('click', () => {
            if (currentPalette.length >= 12) {
                alert('Maximum 12 swatches allowed per palette.');
                return;
            }
            const randomHex = '#' + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0');
            const newObj = {
                name: 'Custom Swatch',
                hex: randomHex,
                rgb: 'rgb(128, 128, 128)',
                rgb_values: [128, 128, 128],
                hsl: 'hsl(0, 0%, 50%)',
                hsl_values: { h: 0, s: 0, l: 50 },
                is_locked: false
            };
            currentPalette.push(newObj);
            updateColorValue(currentPalette.length - 1, randomHex);
            showToast('Added custom swatch!');
        });
    }

    // Update All Studio Panels
    function updateStudioViews() {
        renderCvdPreview();
        renderWcagMatrix();
        populateHarmonySwatchSelector();
        initUiMockupRoleSelectors();
        updateAnalyticsView();
        updateCodeExporterSnippets();
        updateGradientPreview();
        fetchSpatialAnalysis();
        fetchCiede2000Comparison();
        renderRecolorMappingUI();
    }

    // Step 19 & Step 22 Throttled Image Recolor Processor
    const processImageRecolorThrottled = requestAnimationFrameThrottle(processImageRecolor);

    function renderRecolorMappingUI() {
        if (!recolorMappingGrid || !currentPalette.length) return;
        recolorMappingGrid.innerHTML = '';
        recolorTargetMappings = [];

        currentPalette.forEach((c, i) => {
            recolorTargetMappings.push({
                sourceHex: c.hex,
                sourceRgb: c.rgb_values || hexToRgb(c.hex),
                targetHex: c.hex,
                targetRgb: c.rgb_values || hexToRgb(c.hex)
            });

            const card = document.createElement('div');
            card.className = 'recolor-mapping-card';
            card.innerHTML = `
                <div class="recolor-pair">
                    <div class="recolor-swatch-box" style="background-color: ${c.hex}" title="Original: ${c.name}"></div>
                    <i class="fa-solid fa-arrow-right recolor-arrow"></i>
                    <div class="recolor-target-picker">
                        <input type="color" class="native-color-input recolor-target-input" data-index="${i}" value="${c.hex}">
                        <input type="text" class="hex-text-input recolor-target-text" data-index="${i}" value="${c.hex.toUpperCase()}" maxlength="7" style="width:70px;">
                    </div>
                </div>
            `;

            const picker = card.querySelector('.recolor-target-input');
            const textInput = card.querySelector('.recolor-target-text');

            picker.addEventListener('input', (e) => {
                const hex = e.target.value.toLowerCase();
                textInput.value = hex.toUpperCase();
                recolorTargetMappings[i].targetHex = hex;
                recolorTargetMappings[i].targetRgb = hexToRgb(hex);
                processImageRecolorThrottled();
            });

            textInput.addEventListener('change', (e) => {
                let val = e.target.value.trim();
                if (!val.startsWith('#')) val = '#' + val;
                if (/^#([A-Fa-f0-9]{6})$/.test(val)) {
                    val = val.toLowerCase();
                    picker.value = val;
                    recolorTargetMappings[i].targetHex = val;
                    recolorTargetMappings[i].targetRgb = hexToRgb(val);
                    processImageRecolorThrottled();
                } else {
                    e.target.value = recolorTargetMappings[i].targetHex.toUpperCase();
                }
            });

            recolorMappingGrid.appendChild(card);
        });
    }

    if (recolorToleranceSlider) {
        recolorToleranceSlider.addEventListener('input', (e) => {
            if (recolorToleranceVal) recolorToleranceVal.innerText = `${e.target.value}`;
            processImageRecolorThrottled();
        });
    }

    if (recolorPreserveLuminance) {
        recolorPreserveLuminance.addEventListener('change', () => processImageRecolorThrottled());
    }

    if (applyRecolorBtn) {
        applyRecolorBtn.addEventListener('click', () => processImageRecolorThrottled());
    }

    if (resetRecolorBtn) {
        resetRecolorBtn.addEventListener('click', () => {
            renderRecolorMappingUI();
            processImageRecolorThrottled();
            showToast('Reset recolor mappings.');
        });
    }

    if (downloadRecoloredBtn) {
        downloadRecoloredBtn.addEventListener('click', () => {
            if (!recolorResultCanvas) return;
            const link = document.createElement('a');
            link.download = `veyra-recolored-${Date.now()}.png`;
            link.href = recolorResultCanvas.toDataURL('image/png');
            link.click();
            showToast('Downloaded recolored image!');
        });
    }

    function hexToRgb(hex) {
        hex = hex.replace('#', '');
        return [
            parseInt(hex.substring(0, 2), 16),
            parseInt(hex.substring(2, 4), 16),
            parseInt(hex.substring(4, 6), 16)
        ];
    }

    function processImageRecolor() {
        if (!imagePreview.complete || !recolorResultCanvas || !recolorTargetMappings.length) return;

        const width = imagePreview.naturalWidth || imagePreview.clientWidth;
        const height = imagePreview.naturalHeight || imagePreview.clientHeight;

        if (width === 0 || height === 0) return;

        recolorResultCanvas.width = width;
        recolorResultCanvas.height = height;
        const rCtx = recolorResultCanvas.getContext('2d');

        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = width;
        tempCanvas.height = height;
        const tempCtx = tempCanvas.getContext('2d');
        tempCtx.drawImage(imagePreview, 0, 0, width, height);

        const imgData = tempCtx.getImageData(0, 0, width, height);
        const data = imgData.data;

        const tolerance = recolorToleranceSlider ? parseFloat(recolorToleranceSlider.value) : 30;
        const preserveLum = recolorPreserveLuminance ? recolorPreserveLuminance.checked : true;

        for (let i = 0; i < data.length; i += 4) {
            const r = data[i];
            const g = data[i + 1];
            const b = data[i + 2];

            let minDistance = Infinity;
            let closestMapping = null;

            for (let m of recolorTargetMappings) {
                const sRgb = m.sourceRgb;
                const dist = Math.sqrt(
                    (r - sRgb[0]) ** 2 +
                    (g - sRgb[1]) ** 2 +
                    (b - sRgb[2]) ** 2
                );
                if (dist < minDistance) {
                    minDistance = dist;
                    closestMapping = m;
                }
            }

            if (closestMapping && minDistance <= tolerance * 2.55) {
                const targetRgb = closestMapping.targetRgb;
                if (preserveLum) {
                    const origLum = 0.2126 * r + 0.7152 * g + 0.0722 * b;
                    const targetLum = 0.2126 * targetRgb[0] + 0.7152 * targetRgb[1] + 0.0722 * targetRgb[2];
                    const ratio = targetLum > 0 ? origLum / targetLum : 1;

                    data[i] = Math.min(255, Math.max(0, Math.round(targetRgb[0] * ratio)));
                    data[i + 1] = Math.min(255, Math.max(0, Math.round(targetRgb[1] * ratio)));
                    data[i + 2] = Math.min(255, Math.max(0, Math.round(targetRgb[2] * ratio)));
                } else {
                    data[i] = targetRgb[0];
                    data[i + 1] = targetRgb[1];
                    data[i + 2] = targetRgb[2];
                }
            }
        }

        rCtx.putImageData(imgData, 0, 0);
    }

    // Step 18: CIEDE2000 Perceptual Color Matching & Delta E Engine Handlers
    if (ciedeLibrarySelect) {
        ciedeLibrarySelect.addEventListener('change', () => fetchCiede2000Comparison());
    }

    if (ciedeRunCustomBtn) {
        ciedeRunCustomBtn.addEventListener('click', () => {
            const raw = ciedeCustomTargetInput ? ciedeCustomTargetInput.value.trim() : '';
            if (!raw) {
                fetchCiede2000Comparison();
                return;
            }
            const targets = raw.split(',').map(s => s.trim()).filter(Boolean);
            fetchCiede2000Comparison(targets);
        });
    }

    async function fetchCiede2000Comparison(customTargets = null) {
        if (!currentPalette || currentPalette.length === 0 || !ciedeMatchesGrid) return;

        const library = ciedeLibrarySelect ? ciedeLibrarySelect.value : 'tailwind';
        const payload = {
            palette: currentPalette,
            library: library
        };
        if (customTargets && customTargets.length > 0) {
            payload.custom_targets = customTargets;
        }

        try {
            const res = await fetch('/api/compare_ciede2000', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (data.success && data.comparison) {
                renderCiede2000Comparison(data.comparison);
            }
        } catch (err) {
            console.error('Failed to fetch CIEDE2000 comparison:', err);
        }
    }

    function renderCiede2000Comparison(comparison) {
        if (!comparison) return;

        if (ciedeAvgDistVal) {
            ciedeAvgDistVal.innerText = `${comparison.avg_intra_delta_e} ΔE₀₀`;
        }

        if (ciedeMatchesGrid && comparison.closest_matches) {
            ciedeMatchesGrid.innerHTML = '';
            comparison.closest_matches.forEach(match => {
                const card = document.createElement('div');
                card.className = 'ciede-match-card';

                const deltaClass = match.delta_e <= 2.0 ? 'ciede-exact' : (match.delta_e <= 10.0 ? 'ciede-close' : 'ciede-far');

                card.innerHTML = `
                    <div class="ciede-swatch-pair">
                        <div class="ciede-swatch-col">
                            <div class="ciede-color-box" style="background-color: ${match.swatch_hex}"></div>
                            <span class="ciede-color-label" title="${match.swatch_name}">${match.swatch_name}</span>
                            <span class="ciede-hex-sub">${match.swatch_hex.toUpperCase()}</span>
                        </div>
                        <div class="ciede-vs-icon">
                            <i class="fa-solid fa-arrow-right-arrow-left"></i>
                        </div>
                        <div class="ciede-swatch-col">
                            <div class="ciede-color-box" style="background-color: ${match.matched_hex}"></div>
                            <span class="ciede-color-label" title="${match.matched_name}">${match.matched_name}</span>
                            <span class="ciede-hex-sub">${match.matched_hex.toUpperCase()}</span>
                        </div>
                    </div>
                    <div class="ciede-card-footer">
                        <span class="ciede-delta-badge ${deltaClass}">ΔE₀₀: ${match.delta_e}</span>
                        <span class="ciede-interp-tag">${match.interpretation}</span>
                    </div>
                `;
                ciedeMatchesGrid.appendChild(card);
            });
        }

        if (ciedeMatrixTable && comparison.intra_palette_matrix) {
            ciedeMatrixTable.innerHTML = '';

            const matrix = comparison.intra_palette_matrix;

            // Header Row
            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');
            headerRow.innerHTML = '<th>Swatch</th>';
            matrix.forEach((row, i) => {
                const th = document.createElement('th');
                th.innerHTML = `<span class="matrix-header-chip" style="background-color:${row.swatch_hex}" title="${row.swatch_name}">#${i+1}</span>`;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            ciedeMatrixTable.appendChild(thead);

            // Body Rows
            const tbody = document.createElement('tbody');
            matrix.forEach((row, i) => {
                const tr = document.createElement('tr');
                tr.innerHTML = `<td>
                    <div class="matrix-row-label">
                        <span class="matrix-color-dot" style="background-color:${row.swatch_hex}"></span>
                        <span class="matrix-swatch-name">#${i+1} ${row.swatch_name}</span>
                    </div>
                </td>`;

                row.distances.forEach((dist, j) => {
                    const td = document.createElement('td');
                    if (i === j) {
                        td.className = 'matrix-self-cell';
                        td.innerText = '-';
                    } else {
                        td.innerText = dist;
                        if (dist < 10) {
                            td.style.backgroundColor = 'rgba(16, 185, 129, 0.15)';
                            td.style.color = '#10b981';
                        } else if (dist < 25) {
                            td.style.backgroundColor = 'rgba(139, 92, 246, 0.15)';
                            td.style.color = '#8b5cf6';
                        } else {
                            td.style.backgroundColor = 'rgba(245, 158, 11, 0.15)';
                            td.style.color = '#f59e0b';
                        }
                    }
                    tr.appendChild(td);
                });

                tbody.appendChild(tr);
            });
            ciedeMatrixTable.appendChild(tbody);
        }
    }

    // Step 16: Image Spatial Coverage & Pixel Distribution Handlers
    async function fetchSpatialAnalysis() {
        if (!currentFile || !currentPalette.length) return;

        const formData = new FormData();
        formData.append('image', currentFile);
        formData.append('palette', JSON.stringify(currentPalette));
        if (selectedRegion) {
            formData.append('region', JSON.stringify(selectedRegion));
        }

        try {
            const res = await fetch('/api/spatial', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            if (data.success && data.spatial_distribution) {
                renderSpatialDistribution(data.spatial_distribution);
            }
        } catch (err) {
            console.error('Failed to fetch spatial distribution:', err);
        }
    }

    function renderSpatialDistribution(distribution) {
        if (!spatialSummaryBar || !spatialCardsGrid || !distribution) return;

        spatialSummaryBar.innerHTML = '';
        distribution.forEach(item => {
            if (item.percentage <= 0) return;
            const seg = document.createElement('div');
            seg.className = 'coverage-seg';
            seg.style.width = `${item.percentage}%`;
            seg.style.backgroundColor = item.hex;
            seg.title = `${item.name} (${item.hex}): ${item.percentage}% area`;
            if (item.percentage >= 8) {
                seg.innerHTML = `<span>${item.percentage}%</span>`;
            }
            spatialSummaryBar.appendChild(seg);
        });

        spatialCardsGrid.innerHTML = '';
        distribution.forEach(item => {
            const card = document.createElement('div');
            card.className = 'spatial-card';

            card.innerHTML = `
                <div class="spatial-card-header">
                    <div class="spatial-swatch-box" style="background-color: ${item.hex}"></div>
                    <div>
                        <strong style="display:block; font-size:0.9rem;">${item.name}</strong>
                        <span style="font-family:monospace; font-size:0.8rem; color:var(--text-muted);">${item.hex.toUpperCase()}</span>
                    </div>
                </div>
                <div class="spatial-percent-big">${item.percentage}%</div>
                <div class="spatial-role-badge">${item.role_label}</div>
                <div class="spatial-stats-row">
                    <span>Pixel Count: <strong>${item.pixel_count}</strong></span>
                    <span>Centroid: <strong>X:${item.centroid.x}%, Y:${item.centroid.y}%</strong></span>
                </div>
            `;
            spatialCardsGrid.appendChild(card);
        });
    }

    // Step 17 & 22: Multi-Stop CSS Gradient Studio Handlers
    const updateGradientPreviewDebounced = debounce(updateGradientPreview, 100);

    if (gradientTypeSelect) {
        gradientTypeSelect.addEventListener('change', (e) => {
            const val = e.target.value;
            if (gradientAngleGroup) {
                if (val === 'linear') {
                    gradientAngleGroup.classList.remove('hidden');
                } else {
                    gradientAngleGroup.classList.add('hidden');
                }
            }
            updateGradientPreview();
        });
    }

    if (gradientAngleSlider) {
        gradientAngleSlider.addEventListener('input', (e) => {
            if (gradientAngleVal) gradientAngleVal.innerText = `${e.target.value}°`;
            updateGradientPreviewDebounced();
        });
    }

    if (copyGradientCssBtn) {
        copyGradientCssBtn.addEventListener('click', () => {
            if (currentGradientCss) {
                copyToClipboard(currentGradientCss, 'CSS Gradient');
            }
        });
    }

    async function updateGradientPreview() {
        if (!currentPalette.length || !gradientPreviewBox) return;

        const type = gradientTypeSelect ? gradientTypeSelect.value : 'linear';
        const angle = gradientAngleSlider ? gradientAngleSlider.value : 90;

        try {
            const res = await fetch('/api/gradient', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ palette: currentPalette, type: type, angle: angle })
            });
            const data = await res.json();
            if (data.success && data.css) {
                currentGradientCss = data.css;
                gradientPreviewBox.style.cssText = data.css;
            }
        } catch (err) {
            console.error('Failed to fetch gradient CSS:', err);
        }
    }

    // Palette Character & Hue Analytics
    async function updateAnalyticsView() {
        if (!currentPalette || currentPalette.length === 0) return;

        try {
            const response = await fetch('/api/analytics', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ palette: currentPalette })
            });
            const data = await response.json();
            if (data.success && data.analytics) {
                renderAnalytics(data.analytics);
            }
        } catch (err) {
            console.error('Failed to fetch analytics:', err);
        }
    }

    function renderAnalytics(analytics) {
        if (!analytics) return;
        if (analyticsProfileTitle) analyticsProfileTitle.innerText = analytics.profile || 'Standard Palette';
        if (analyticsProfileDesc) analyticsProfileDesc.innerText = analytics.description || '';
        if (metricDomHue) metricDomHue.innerText = analytics.dominant_hue_name || 'None';
        if (metricAvgSat) metricAvgSat.innerText = `${analytics.avg_saturation ?? 0}%`;
        if (metricAvgLight) metricAvgLight.innerText = `${analytics.avg_lightness ?? 0}%`;
        if (metricLightRange) metricLightRange.innerText = `${analytics.lightness_range ?? 0}%`;

        if (hueDistributionBars && analytics.hue_distribution) {
            hueDistributionBars.innerHTML = '';
            analytics.hue_distribution.forEach(item => {
                const row = document.createElement('div');
                row.className = 'hue-bar-item';
                row.innerHTML = `
                    <div class="hue-bar-label-row">
                        <span class="hue-bar-name">
                            <span class="hue-color-dot" style="background-color: ${item.sample}"></span>
                            ${item.name} (${item.count} swatch${item.count > 1 ? 'es' : ''})
                        </span>
                        <span style="color: var(--text-muted);">${item.percentage}%</span>
                    </div>
                    <div class="hue-bar-track">
                        <div class="hue-bar-fill" style="width: ${item.percentage}%; background-color: ${item.sample};"></div>
                    </div>
                `;
                hueDistributionBars.appendChild(row);
            });
        }
    }

    // CVD Preview Simulation Renderer
    function renderCvdPreview() {
        if (!currentPalette.length || !cvdPreviewGrid) return;
        cvdPreviewGrid.innerHTML = '';
        const mode = cvdSelect ? cvdSelect.value : 'normal';

        currentPalette.forEach(color => {
            const hex = (mode === 'normal') ? color.hex : (color.cvd_simulations ? color.cvd_simulations[mode] : color.hex);
            const card = document.createElement('div');
            card.className = 'swatch-card';
            card.innerHTML = `
                <div class="swatch-box" style="background-color: ${hex}"></div>
                <div class="swatch-info">
                    <span class="swatch-name-tag" title="${color.name || 'Swatch'}">${color.name || 'Swatch'}</span>
                    <div class="copy-badge" data-copy="${hex}">
                        <span class="label">${mode.slice(0, 4)}</span>
                        <span class="val">${hex}</span>
                    </div>
                </div>
            `;
            cvdPreviewGrid.appendChild(card);
        });
    }

    if (cvdSelect) {
        cvdSelect.addEventListener('change', renderCvdPreview);
    }

    // WCAG 2.1 Legibility Matrix Renderer
    function renderWcagMatrix() {
        if (!currentPalette.length || !wcagMatrixGrid) return;
        wcagMatrixGrid.innerHTML = '';

        currentPalette.forEach(color => {
            const acc = color.accessibility;
            if (!acc) return;

            const card = document.createElement('div');
            card.className = 'wcag-card';

            const bestText = acc.best_text_color;
            const whiteRatio = acc.contrast_white;
            const blackRatio = acc.contrast_black;

            card.innerHTML = `
                <div class="wcag-preview" style="background-color: ${color.hex}; color: ${bestText}">
                    ${color.name || 'Sample Text'} (${color.hex})
                </div>
                <div class="wcag-details">
                    <div><strong>VS White (#FFF):</strong> ${whiteRatio}:1
                        <span class="badge ${acc.wcag_white.aa_normal ? 'badge-pass' : 'badge-fail'}">AA ${acc.wcag_white.aa_normal ? 'PASS' : 'FAIL'}</span>
                        <span class="badge ${acc.wcag_white.aaa_normal ? 'badge-pass' : 'badge-fail'}">AAA ${acc.wcag_white.aaa_normal ? 'PASS' : 'FAIL'}</span>
                    </div>
                    <div><strong>VS Black (#000):</strong> ${blackRatio}:1
                        <span class="badge ${acc.wcag_black.aa_normal ? 'badge-pass' : 'badge-fail'}">AA ${acc.wcag_black.aa_normal ? 'PASS' : 'FAIL'}</span>
                        <span class="badge ${acc.wcag_black.aaa_normal ? 'badge-pass' : 'badge-fail'}">AAA ${acc.wcag_black.aaa_normal ? 'PASS' : 'FAIL'}</span>
                    </div>
                </div>
            `;
            wcagMatrixGrid.appendChild(card);
        });
    }

    // Color Harmonies Generator Handler
    function populateHarmonySwatchSelector() {
        if (!currentPalette.length || !harmonySwatchSelect) return;
        harmonySwatchSelect.innerHTML = '';

        currentPalette.forEach((c, idx) => {
            const opt = document.createElement('option');
            opt.value = idx;
            opt.innerText = `${c.name || 'Swatch ' + (idx + 1)} (${c.hex})`;
            harmonySwatchSelect.appendChild(opt);
        });

        fetchAndRenderHarmonies(currentPalette[0]);
    }

    if (harmonySwatchSelect) {
        harmonySwatchSelect.addEventListener('change', (e) => {
            const selectedColor = currentPalette[e.target.value];
            if (selectedColor) fetchAndRenderHarmonies(selectedColor);
        });
    }

    async function fetchAndRenderHarmonies(color) {
        if (!harmoniesContainer) return;
        try {
            const response = await fetch('/api/harmonies', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ rgb_values: color.rgb_values, hex: color.hex })
            });
            const data = await response.json();
            if (data.success) {
                renderHarmonies(data.harmonies);
            }
        } catch (err) {
            console.error('Failed to load harmonies:', err);
        }
    }

    function renderHarmonies(harmonies) {
        if (!harmoniesContainer) return;
        harmoniesContainer.innerHTML = '';
        const types = ['complementary', 'analogous', 'triadic', 'split_complementary'];

        types.forEach(type => {
            const colors = harmonies[type];
            if (!colors) return;

            const block = document.createElement('div');
            block.className = 'harmony-block';
            block.innerHTML = `
                <h4>${type.replace('_', ' ')}</h4>
                <div class="harmony-row"></div>
            `;

            const row = block.querySelector('.harmony-row');
            colors.forEach(c => {
                const swatch = document.createElement('div');
                swatch.className = 'harmony-swatch';
                swatch.style.backgroundColor = c.hex;
                swatch.style.color = c.accessibility ? c.accessibility.best_text_color : '#ffffff';
                swatch.innerHTML = `
                    <span>${c.hex}</span>
                    <span class="harmony-name-sub">${c.name || ''}</span>
                `;
                swatch.addEventListener('click', () => copyToClipboard(c.hex, `${c.name || 'HEX'}: ${c.hex}`));
                row.appendChild(swatch);
            });

            harmoniesContainer.appendChild(block);
        });
    }

    // Interactive UI Component Sandbox Mapping
    function initUiMockupRoleSelectors() {
        if (!currentPalette.length) return;

        Object.values(roleSelects).forEach(select => {
            if (select) {
                select.innerHTML = '';
                currentPalette.forEach((c, idx) => {
                    const opt = document.createElement('option');
                    opt.value = c.hex;
                    opt.innerText = `${c.name || 'Swatch ' + (idx + 1)} (${c.hex})`;
                    select.appendChild(opt);
                });
            }
        });

        const sortedByLightness = [...currentPalette].sort((a, b) => (a.hsl_values?.l || 0) - (b.hsl_values?.l || 0));
        const bgHex = sortedByLightness[0].hex;
        const textHex = sortedByLightness[sortedByLightness.length - 1].hex;

        const surfaceHex = currentPalette[1] ? currentPalette[1].hex : bgHex;
        const primaryHex = currentPalette[0] ? currentPalette[0].hex : textHex;
        const accentHex = currentPalette[currentPalette.length - 2] ? currentPalette[currentPalette.length - 2].hex : primaryHex;

        if (roleSelects.bg) roleSelects.bg.value = bgHex;
        if (roleSelects.surface) roleSelects.surface.value = surfaceHex;
        if (roleSelects.primary) roleSelects.primary.value = primaryHex;
        if (roleSelects.accent) roleSelects.accent.value = accentHex;
        if (roleSelects.text) roleSelects.text.value = textHex;

        applyMockupStyles();
    }

    function applyMockupStyles() {
        if (!uiMockupFrame) return;
        if (roleSelects.bg) uiMockupFrame.style.setProperty('--preview-bg', roleSelects.bg.value);
        if (roleSelects.surface) uiMockupFrame.style.setProperty('--preview-surface', roleSelects.surface.value);
        if (roleSelects.primary) uiMockupFrame.style.setProperty('--preview-primary', roleSelects.primary.value);
        if (roleSelects.accent) uiMockupFrame.style.setProperty('--preview-accent', roleSelects.accent.value);
        if (roleSelects.text) uiMockupFrame.style.setProperty('--preview-text', roleSelects.text.value);
    }

    Object.values(roleSelects).forEach(select => {
        if (select) {
            select.addEventListener('change', applyMockupStyles);
        }
    });

    // Code Exporters & Token Exporters API Handlers
    async function updateCodeExporterSnippets() {
        if (!currentPalette.length) return;

        try {
            const [twRes, scssRes, figmaRes] = await Promise.all([
                fetch('/api/export/tailwind', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ palette: currentPalette })
                }),
                fetch('/api/export/scss', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ palette: currentPalette })
                }),
                fetch('/api/export/figma', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ palette: currentPalette })
                })
            ]);

            const twData = await twRes.json();
            const scssData = await scssRes.json();
            const figmaData = await figmaRes.json();

            generatedCodeSnippets = {
                tailwind: twData.content || '',
                scss: scssData.content || '',
                figma: figmaData.content || ''
            };

            renderCodeOutput();
        } catch (err) {
            console.error('Failed to fetch code snippets:', err);
        }
    }

    function renderCodeOutput() {
        if (codeOutputBlock && generatedCodeSnippets[activeCodeFormat]) {
            codeOutputBlock.innerText = generatedCodeSnippets[activeCodeFormat];
        }
    }

    codeTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            codeTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            activeCodeFormat = tab.getAttribute('data-code');
            renderCodeOutput();
        });
    });

    if (copyCodeBtn) {
        copyCodeBtn.addEventListener('click', () => {
            const snippet = generatedCodeSnippets[activeCodeFormat];
            if (snippet) {
                copyToClipboard(snippet, `${activeCodeFormat.toUpperCase()} Code Snippet`);
            }
        });
    }

    if (exportAseBtn) {
        exportAseBtn.addEventListener('click', () => downloadBinaryExport('ase'));
    }

    if (exportSvgBtn) {
        exportSvgBtn.addEventListener('click', () => downloadBinaryExport('svg'));
    }

    async function downloadBinaryExport(fmt) {
        if (!currentPalette.length) {
            alert('Extract a palette first.');
            return;
        }

        try {
            const response = await fetch(`/api/export/${fmt}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ palette: currentPalette })
            });

            if (!response.ok) throw new Error('Download failed');

            const blob = await response.blob();
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `veyra-palette.${fmt}`;
            link.click();
            URL.revokeObjectURL(link.href);
            showToast(`Downloaded .${fmt.toUpperCase()} export!`);
        } catch (err) {
            alert(`Failed to download .${fmt} file.`);
        }
    }

    // Local Palette History & Favorites Storage Manager
    function getStoredHistory() {
        try {
            const data = localStorage.getItem('veyra_palette_history');
            return data ? JSON.parse(data) : [];
        } catch (e) {
            return [];
        }
    }

    function saveStoredHistory(history) {
        try {
            localStorage.setItem('veyra_palette_history', JSON.stringify(history));
        } catch (e) {
            console.error('Failed to save palette to localStorage:', e);
        }
    }

    function autoSaveToHistory(palette) {
        if (!palette || !palette.length) return;
        const history = getStoredHistory();

        const existingIdx = history.findIndex(item => item.id === currentPaletteId);
        const itemObj = {
            id: currentPaletteId || ('pal_' + Date.now()),
            timestamp: new Date().toLocaleString([], { dateStyle: 'short', timeStyle: 'short' }),
            is_favorite: existingIdx >= 0 ? history[existingIdx].is_favorite : false,
            palette: palette
        };

        if (existingIdx >= 0) {
            history[existingIdx] = itemObj;
        } else {
            history.unshift(itemObj);
        }

        if (history.length > 25) history.pop();
        saveStoredHistory(history);
        updateSaveFavoriteButtonState(itemObj.is_favorite);
    }

    function toggleFavoriteCurrentPalette() {
        if (!currentPalette.length) return;
        const history = getStoredHistory();
        const existing = history.find(item => item.id === currentPaletteId);

        let isFav = false;
        if (existing) {
            existing.is_favorite = !existing.is_favorite;
            isFav = existing.is_favorite;
            saveStoredHistory(history);
        } else {
            isFav = true;
            const newItem = {
                id: currentPaletteId || ('pal_' + Date.now()),
                timestamp: new Date().toLocaleString([], { dateStyle: 'short', timeStyle: 'short' }),
                is_favorite: true,
                palette: currentPalette
            };
            history.unshift(newItem);
            saveStoredHistory(history);
        }

        updateSaveFavoriteButtonState(isFav);
        showToast(isFav ? 'Added to Saved Favorites!' : 'Removed from Favorites');
        renderHistoryGrid();
    }

    function updateSaveFavoriteButtonState(isFavorite) {
        if (!savePaletteBtn) return;
        const icon = savePaletteBtn.querySelector('i');
        if (isFavorite) {
            savePaletteBtn.classList.add('active');
            if (icon) icon.className = 'fa-solid fa-star';
            savePaletteBtn.innerHTML = '<i class="fa-solid fa-star"></i> Favorited';
        } else {
            savePaletteBtn.classList.remove('active');
            if (icon) icon.className = 'fa-regular fa-star';
            savePaletteBtn.innerHTML = '<i class="fa-regular fa-star"></i> Save Favorite';
        }
    }

    if (savePaletteBtn) {
        savePaletteBtn.addEventListener('click', toggleFavoriteCurrentPalette);
    }

    function renderHistoryGrid() {
        if (!historyGrid) return;
        const history = getStoredHistory();
        const filter = historyFilterSelect ? historyFilterSelect.value : 'all';

        const filtered = history.filter(item => {
            if (filter === 'favorites') return item.is_favorite;
            return true;
        });

        historyGrid.innerHTML = '';

        if (filtered.length === 0) {
            historyGrid.innerHTML = `<div class="empty-history-msg"><i class="fa-solid fa-box-open" style="font-size:2rem; margin-bottom:0.5rem; display:block;"></i>No ${filter === 'favorites' ? 'favorite' : 'saved'} palettes found in history.</div>`;
            return;
        }

        filtered.forEach(item => {
            const card = document.createElement('div');
            card.className = 'history-card';

            const swatchStrips = item.palette.map(c => `<div class="history-swatch-seg" style="background-color: ${c.hex}" title="${c.name || c.hex}"></div>`).join('');

            card.innerHTML = `
                <div class="history-swatches-strip">${swatchStrips}</div>
                <div class="history-meta">
                    <span>${item.palette.length} Colors • ${item.timestamp}</span>
                </div>
                <div class="history-card-actions">
                    <button type="button" class="btn-action btn-fav-card" title="Toggle Favorite">
                        <i class="${item.is_favorite ? 'fa-solid fa-star' : 'fa-regular fa-star'}"></i>
                    </button>
                    <button type="button" class="btn-action btn-load-card">
                        <i class="fa-solid fa-folder-open"></i> Load
                    </button>
                    <button type="button" class="btn-action btn-del-card" title="Delete">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            `;

            card.querySelector('.btn-fav-card').addEventListener('click', () => {
                item.is_favorite = !item.is_favorite;
                saveStoredHistory(history);
                if (item.id === currentPaletteId) updateSaveFavoriteButtonState(item.is_favorite);
                renderHistoryGrid();
            });

            card.querySelector('.btn-load-card').addEventListener('click', () => {
                currentPalette = item.palette;
                currentPaletteId = item.id;
                renderPalette(currentPalette);
                updateStudioViews();
                updateSaveFavoriteButtonState(item.is_favorite);

                studioTabs.forEach(t => t.classList.remove('active'));
                tabPanes.forEach(p => p.classList.add('hidden'));
                const mainGridTab = document.querySelector('.studio-tab[data-target="tab-grid"]');
                const mainGridPane = document.getElementById('tab-grid');
                if (mainGridTab) mainGridTab.classList.add('active');
                if (mainGridPane) mainGridPane.classList.remove('hidden');

                showToast('Loaded palette into studio!');
            });

            card.querySelector('.btn-del-card').addEventListener('click', () => {
                const updated = history.filter(h => h.id !== item.id);
                saveStoredHistory(updated);
                renderHistoryGrid();
                showToast('Deleted palette from history.');
            });

            historyGrid.appendChild(card);
        });
    }

    if (historyFilterSelect) {
        historyFilterSelect.addEventListener('change', renderHistoryGrid);
    }

    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', () => {
            if (confirm('Are you sure you want to clear all palette history?')) {
                localStorage.removeItem('veyra_palette_history');
                renderHistoryGrid();
                showToast('Cleared palette history.');
            }
        });
    }

    // Bulk Actions & Downloads
    if (copyHexListBtn) {
        copyHexListBtn.addEventListener('click', () => {
            if (!currentPalette.length) return;
            const hexList = currentPalette.map(c => c.hex).join(', ');
            copyToClipboard(hexList, 'All HEX codes');
        });
    }

    if (downloadPngBtn) downloadPngBtn.addEventListener('click', exportPaletteAsPngCard);

    if (downloadCssBtn) {
        downloadCssBtn.addEventListener('click', () => {
            if (!currentPalette.length) return;
            const cssVars = currentPalette.map((c, i) => `  --${(c.name || 'color-' + (i + 1)).toLowerCase().replace(/\s+/g, '-')}: ${c.hex};`).join('\n');
            const cssContent = `:root {\n${cssVars}\n}`;
            triggerFileDownload('veyra-palette.css', cssContent, 'text/css');
        });
    }

    if (downloadJsonBtn) {
        downloadJsonBtn.addEventListener('click', () => {
            if (!currentPalette.length) return;
            const jsonStr = JSON.stringify(currentPalette.map(c => ({
                name: c.name,
                hex: c.hex,
                rgb: c.rgb,
                hsl: c.hsl,
                wcag: c.accessibility
            })), null, 2);
            triggerFileDownload('veyra-palette.json', jsonStr, 'application/json');
        });
    }

    function exportPaletteAsPngCard() {
        if (!currentPalette || currentPalette.length === 0) return;

        const offCanvas = document.createElement('canvas');
        const oCtx = offCanvas.getContext('2d');

        const swatchWidth = 140;
        const swatchHeight = 190;
        const padding = 30;
        const headerHeight = 70;
        const footerHeight = 40;

        const totalWidth = (swatchWidth * currentPalette.length) + (padding * 2);
        const totalHeight = headerHeight + swatchHeight + footerHeight + padding;

        offCanvas.width = totalWidth;
        offCanvas.height = totalHeight;

        oCtx.fillStyle = '#0f172a';
        oCtx.fillRect(0, 0, totalWidth, totalHeight);

        oCtx.fillStyle = '#8b5cf6';
        oCtx.font = 'bold 22px "Segoe UI", sans-serif';
        oCtx.fillText('VEYRA PALETTE STUDIO', padding, 45);

        oCtx.fillStyle = '#94a3b8';
        oCtx.font = '13px "Segoe UI", sans-serif';
        oCtx.fillText(`${currentPalette.length} Swatches • Extracted Palette`, totalWidth - padding - 220, 44);

        currentPalette.forEach((color, i) => {
            const x = padding + (i * swatchWidth);
            const y = headerHeight;

            oCtx.fillStyle = color.hex;
            oCtx.fillRect(x + 4, y, swatchWidth - 8, swatchHeight - 55);

            oCtx.fillStyle = '#1e293b';
            oCtx.fillRect(x + 4, y + swatchHeight - 55, swatchWidth - 8, 55);

            oCtx.fillStyle = '#8b5cf6';
            oCtx.font = 'bold 11px "Segoe UI", sans-serif';
            oCtx.textAlign = 'center';
            oCtx.fillText((color.name || '').toUpperCase(), x + (swatchWidth / 2), y + swatchHeight - 32);

            oCtx.fillStyle = '#f8fafc';
            oCtx.font = 'bold 13px monospace';
            oCtx.fillText(color.hex.toUpperCase(), x + (swatchWidth / 2), y + swatchHeight - 14);
        });

        oCtx.fillStyle = '#475569';
        oCtx.font = '11px "Segoe UI", sans-serif';
        oCtx.textAlign = 'left';
        oCtx.fillText('Generated with Veyra Palette Studio', padding, totalHeight - 15);

        const link = document.createElement('a');
        link.download = `veyra-palette-${Date.now()}.png`;
        link.href = offCanvas.toDataURL('image/png');
        link.click();
        showToast('Downloaded PNG Palette Card!');
    }

    function triggerFileDownload(filename, content, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const link = document.createElement('a');
        link.download = filename;
        link.href = URL.createObjectURL(blob);
        link.click();
        URL.revokeObjectURL(link.href);
        showToast(`Downloaded ${filename}!`);
    }

    function copyToClipboard(text, description) {
        navigator.clipboard.writeText(text).then(() => {
            showToast(`Copied ${description}!`);
        }).catch(() => {
            alert(`Failed to copy ${description}.`);
        });
    }

    function showToast(msg) {
        if (!toast || !toastMessage) return;
        toastMessage.innerText = msg;
        toast.classList.remove('hidden');
        toast.style.opacity = '1';

        if (toastTimeout) clearTimeout(toastTimeout);
        toastTimeout = setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.classList.add('hidden'), 300);
        }, 2200);
    }
});