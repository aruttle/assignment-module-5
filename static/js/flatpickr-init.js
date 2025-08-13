document.addEventListener('DOMContentLoaded', function () {
  // Safeguard if this page doesn't include flatpickr
  if (typeof flatpickr !== 'function') return;

  // Pull booked ranges (from accommodation_detail template)
  let bookedRanges = [];
  const jsonScript = document.getElementById('booked-ranges-data');
  if (jsonScript) {
    try {
      bookedRanges = JSON.parse(jsonScript.textContent || '[]') || [];
    } catch (e) {
      console.error('Error parsing booked ranges JSON:', e);
    }
  }

  // Build disable list for flatpickr
  const disableRanges = (bookedRanges || []).map(r => ({
    from: r.from,
    to: r.to
  }));

  // Find inputs robustly (name OR id)
  const checkInEl =
    document.querySelector('input[name="check_in"]') ||
    document.getElementById('id_check_in') ||
    document.getElementById('check_in');

  const checkOutEl =
    document.querySelector('input[name="check_out"]') ||
    document.getElementById('id_check_out') ||
    document.getElementById('check_out');

  // Shared config
  const baseConfig = {
    dateFormat: 'Y-m-d',
    minDate: 'today',
    disable: disableRanges,
    altInput: true,
    altFormat: 'D, M j, Y',
  };

  let fpCheckIn = null;
  let fpCheckOut = null;

  if (checkInEl) {
    fpCheckIn = flatpickr(checkInEl, {
      ...baseConfig,
      onChange: function (selectedDates, dateStr) {
        // When check-in changes, push min date on check-out
        if (fpCheckOut && selectedDates.length) {
          fpCheckOut.set('minDate', selectedDates[0]);
          // If current check-out < new check-in, clear it
          const outDate = fpCheckOut.selectedDates[0];
          if (outDate && outDate < selectedDates[0]) {
            fpCheckOut.clear();
          }
        }
      }
    });
  }

  if (checkOutEl) {
    fpCheckOut = flatpickr(checkOutEl, {
      ...baseConfig
    });

    // If we already picked a check-in (server-side initial), respect it
    if (fpCheckIn && fpCheckIn.selectedDates.length) {
      fpCheckOut.set('minDate', fpCheckIn.selectedDates[0]);
    }
  }
});
