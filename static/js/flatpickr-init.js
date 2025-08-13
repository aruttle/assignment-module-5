document.addEventListener('DOMContentLoaded', function () {
  // 1) Read booked ranges JSON if present
  const jsonScript = document.getElementById('booked-ranges-data');
  let bookedRanges = [];
  if (jsonScript) {
    try {
      bookedRanges = JSON.parse(jsonScript.textContent || '[]');
    } catch (e) {
      console.error("Error parsing booked ranges JSON:", e);
    }
  }

  // 2) Build config (disable already booked ranges)
  const baseConfig = {
    dateFormat: "Y-m-d",
    minDate: "today",
    disable: bookedRanges.map(r => ({ from: r.from, to: r.to })),
    allowInput: true
  };

  // 3) Find inputs by id OR name (be tolerant)
  const checkInEl  = document.querySelector('#id_check_in, [name="check_in"], #check_in');
  const checkOutEl = document.querySelector('#id_check_out, [name="check_out"], #check_out');

  if (!checkInEl && !checkOutEl) {
    // No booking fields on this page — nothing to do
    return;
  }

  // 4) Initialize pickers
  let fpIn = null, fpOut = null;

  if (checkInEl) {
    fpIn = flatpickr(checkInEl, { ...baseConfig });
  }
  if (checkOutEl) {
    fpOut = flatpickr(checkOutEl, { ...baseConfig });
  }

  // 5) Link min date of check-out to the selected check-in
  if (fpIn && fpOut) {
    checkInEl.addEventListener('change', () => {
      const val = checkInEl.value ? new Date(checkInEl.value) : "today";
      fpOut.set('minDate', val);
    });
  }
});
