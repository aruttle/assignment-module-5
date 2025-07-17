document.addEventListener('DOMContentLoaded', () => {
  const accommodations = JSON.parse(document.getElementById('accommodations-data').textContent);
  const bookedRangesByAccommodation = JSON.parse(document.getElementById('booked-ranges-data').textContent);

  const accommodationTypeSelect = document.getElementById('accommodation_type');
  const accommodationSelect = document.getElementById('accommodation');

  const startInput = document.getElementById('start_date');
  const endInput = document.getElementById('end_date');

  let startPicker = null;
  let endPicker = null;

  // Disable date inputs initially
  startInput.disabled = true;
  endInput.disabled = true;

  function populateAccommodations(typeId) {
    accommodationSelect.innerHTML = '<option value="" disabled selected>Select accommodation</option>';
    accommodations.forEach(acc => {
      if (acc.type_id == typeId) {
        const option = document.createElement('option');
        option.value = acc.id;
        option.textContent = acc.name;
        accommodationSelect.appendChild(option);
      }
    });
    // Reset date inputs and destroy pickers when accommodation list changes
    resetDatePickers();
  }

  function resetDatePickers() {
    if (startPicker) {
      startPicker.destroy();
      startPicker = null;
    }
    if (endPicker) {
      endPicker.destroy();
      endPicker = null;
    }
    startInput.value = '';
    endInput.value = '';
    startInput.disabled = true;
    endInput.disabled = true;
  }

  function updateFlatpickr(accommodationId) {
    const ranges = bookedRangesByAccommodation[accommodationId] || [];

    const disableRanges = ranges.map(range => ({
      from: range.start,
      to: range.end
    }));

    // Destroy previous pickers before re-creating
    if (startPicker) startPicker.destroy();
    if (endPicker) endPicker.destroy();

    startPicker = flatpickr("#start_date", {
      dateFormat: 'Y-m-d',
      minDate: 'today',  // Prevent past dates
      disable: disableRanges,
      onChange(selectedDates) {
        if (selectedDates.length > 0) {
          const minEndDate = selectedDates[0];
          endPicker.set('minDate', minEndDate);
          if (endPicker.selectedDates.length > 0 && endPicker.selectedDates[0] < minEndDate) {
            endPicker.clear();
          }
        }
      }
    });

    endPicker = flatpickr("#end_date", {
      dateFormat: 'Y-m-d',
      minDate: 'today',  // Prevent past dates
      disable: disableRanges,
    });

    // Enable date inputs now that accommodation is selected
    startInput.disabled = false;
    endInput.disabled = false;
  }

  accommodationTypeSelect.addEventListener('change', function () {
    const selectedTypeId = this.value;
    populateAccommodations(selectedTypeId);
  });

  accommodationSelect.addEventListener('change', function () {
    const selectedAccommodationId = this.value;
    if (selectedAccommodationId) {
      updateFlatpickr(selectedAccommodationId);
    } else {
      resetDatePickers();
    }
  });

  // On page load, if accommodation type is already selected, populate accommodations
  if (accommodationTypeSelect.value) {
    populateAccommodations(accommodationTypeSelect.value);
  }
});
