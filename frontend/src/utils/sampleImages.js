// Generates valid in-memory construction sample images via HTML5 Canvas
export function createConstructionSampleImage(type = "safety_deck") {
  const canvas = document.createElement("canvas");
  canvas.width = 640;
  canvas.height = 480;
  const ctx = canvas.getContext("2d");

  if (type === "safety_deck") {
    // Sky gradient
    const skyGrad = ctx.createLinearGradient(0, 0, 0, 240);
    skyGrad.addColorStop(0, "#1e293b");
    skyGrad.addColorStop(1, "#334155");
    ctx.fillStyle = skyGrad;
    ctx.fillRect(0, 0, 640, 480);

    // Concrete slab deck
    ctx.fillStyle = "#64748b";
    ctx.fillRect(0, 280, 640, 200);

    // Rebar grid lines
    ctx.strokeStyle = "#94a3b8";
    ctx.lineWidth = 2;
    for (let x = 20; x < 640; x += 30) {
      ctx.beginPath();
      ctx.moveTo(x, 280);
      ctx.lineTo(x, 480);
      ctx.stroke();
    }
    for (let y = 300; y < 480; y += 25) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(640, y);
      ctx.stroke();
    }

    // Scaffolding column
    ctx.strokeStyle = "#e2e8f0";
    ctx.lineWidth = 4;
    ctx.strokeRect(80, 80, 100, 200);
    ctx.beginPath();
    ctx.moveTo(80, 80);
    ctx.lineTo(180, 280);
    ctx.moveTo(180, 80);
    ctx.lineTo(80, 280);
    ctx.stroke();

    // Tower Crane arm
    ctx.strokeStyle = "#f59e0b";
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(350, 40);
    ctx.lineTo(620, 120);
    ctx.stroke();

    // Worker silhouettes
    // Worker 1: compliant with yellow helmet and orange vest
    ctx.fillStyle = "#fbbf24"; // Hard hat
    ctx.beginPath();
    ctx.arc(260, 230, 14, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#ea580c"; // High-vis vest
    ctx.fillRect(248, 246, 24, 38);
    ctx.fillStyle = "#1e293b"; // Legs
    ctx.fillRect(250, 284, 9, 35);
    ctx.fillRect(261, 284, 9, 35);

    // Worker 2: on edge without harness (hazard)
    ctx.fillStyle = "#ef4444"; // Warning red
    ctx.beginPath();
    ctx.arc(540, 235, 14, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#334155";
    ctx.fillRect(530, 250, 20, 36);
    ctx.fillRect(532, 286, 7, 32);
    ctx.fillRect(541, 286, 7, 32);

    // Overlay Tag
    ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
    ctx.fillRect(20, 20, 280, 40);
    ctx.fillStyle = "#f59e0b";
    ctx.font = "bold 14px 'Plus Jakarta Sans', sans-serif";
    ctx.fillText("SITE AUDIT: SLAB DECK LEVEL 14", 30, 45);

  } else if (type === "crack_shear") {
    // Concrete background
    ctx.fillStyle = "#475569";
    ctx.fillRect(0, 0, 640, 480);

    // Concrete texture specks
    ctx.fillStyle = "#334155";
    for (let i = 0; i < 400; i++) {
      ctx.fillRect(Math.random() * 640, Math.random() * 480, 2, 2);
    }

    // 45 degree diagonal shear crack
    ctx.strokeStyle = "#0f172a";
    ctx.lineWidth = 6;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.beginPath();
    ctx.moveTo(140, 100);
    ctx.lineTo(210, 170);
    ctx.lineTo(240, 190);
    ctx.lineTo(320, 270);
    ctx.lineTo(370, 305);
    ctx.lineTo(460, 390);
    ctx.stroke();

    // Secondary hairline fissures
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(240, 190);
    ctx.lineTo(270, 180);
    ctx.moveTo(320, 270);
    ctx.lineTo(340, 310);
    ctx.stroke();

    // Measurement scale marker
    ctx.fillStyle = "#f59e0b";
    ctx.fillRect(100, 400, 150, 12);
    ctx.fillStyle = "#ffffff";
    ctx.font = "12px monospace";
    ctx.fillText("100mm GAUGE SCALE", 115, 430);

    // Crack tag
    ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
    ctx.fillRect(20, 20, 340, 40);
    ctx.fillStyle = "#ef4444";
    ctx.font = "bold 14px 'Plus Jakarta Sans', sans-serif";
    ctx.fillText("DEFECT: 45° DIAGONAL SHEAR CRACK (3.4mm)", 30, 45);

  } else if (type === "crack_settlement") {
    // Brick pattern
    ctx.fillStyle = "#7c2d12";
    ctx.fillRect(0, 0, 640, 480);

    // Mortar lines
    ctx.strokeStyle = "#cbd5e1";
    ctx.lineWidth = 3;
    for (let y = 0; y < 480; y += 40) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(640, y);
      ctx.stroke();
      const offset = (y % 80 === 0) ? 0 : 50;
      for (let x = offset; x < 640; x += 100) {
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x, y + 40);
        ctx.stroke();
      }
    }

    // Stepped settlement crack
    ctx.strokeStyle = "#000000";
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(100, 40);
    ctx.lineTo(150, 40);
    ctx.lineTo(150, 80);
    ctx.lineTo(250, 80);
    ctx.lineTo(250, 160);
    ctx.lineTo(350, 160);
    ctx.lineTo(350, 240);
    ctx.lineTo(450, 240);
    ctx.lineTo(450, 360);
    ctx.lineTo(520, 440);
    ctx.stroke();

    ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
    ctx.fillRect(20, 20, 320, 40);
    ctx.fillStyle = "#f59e0b";
    ctx.font = "bold 14px 'Plus Jakarta Sans', sans-serif";
    ctx.fillText("DEFECT: STEPPED SETTLEMENT CRACK", 30, 45);

  } else {
    // Default high-rise excavation
    ctx.fillStyle = "#78350f";
    ctx.fillRect(0, 200, 640, 280);
    ctx.fillStyle = "#38bdf8";
    ctx.fillRect(0, 0, 640, 200);

    // Excavator arm
    ctx.strokeStyle = "#eab308";
    ctx.lineWidth = 14;
    ctx.beginPath();
    ctx.moveTo(180, 260);
    ctx.lineTo(280, 160);
    ctx.lineTo(360, 220);
    ctx.stroke();

    ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
    ctx.fillRect(20, 20, 310, 40);
    ctx.fillStyle = "#10b981";
    ctx.font = "bold 14px 'Plus Jakarta Sans', sans-serif";
    ctx.fillText("SITE ZONE: EXCAVATION PIT (COMPLIANT)", 30, 45);
  }

  const dataUrl = canvas.toDataURL("image/jpeg", 0.92);
  const arr = dataUrl.split(",");
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  const blob = new Blob([u8arr], { type: mime });
  const file = new File([blob], `${type}.jpg`, { type: mime });
  return Promise.resolve({ file, previewUrl: dataUrl });
}
