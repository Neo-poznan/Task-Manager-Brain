const contentWrapper = document.querySelector('.statistics-wrapper');
const contents = document.querySelectorAll('.content');
const nextButton = document.getElementById('btnNext');
const prevButton = document.getElementById('btnPrev');

let currentIndex = 0;

nextButton.addEventListener('click', () => {
    // Увеличиваем индекс текущего контента
    currentIndex = (currentIndex + 1) % contents.length;

    // Смещаем wrapper влево на ширину одного контента
    contentWrapper.style.transform = `translateX(-${currentIndex * 500}px)`;
});

prevButton.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + contents.length) % contents.length;
    contentWrapper.style.transform = `translateX(-${currentIndex * 500}px)`;
});

const countUserTasksInCategoriesCTX = document.getElementById('countUserTasksInCategoriesChart');

const countUserTasksInCategoriesChartData = {
  labels: countUserTasksInCategories.labels,
  datasets: [{
    label: 'Задач в категории',
    data: countUserTasksInCategories.data,
    backgroundColor: countUserTasksInCategories.colors,
    hoverOffset: 4
  }]
};

const countUserTasksInCategoriesConfig = {
    type: 'doughnut',
    data: countUserTasksInCategoriesChartData,
    options: { elements: { arc: { borderColor: "rgb(15, 15, 15)" } } }

}

new Chart(countUserTasksInCategoriesCTX, countUserTasksInCategoriesConfig);

const userAccuracyByCategoriesCTX = document.getElementById('userAccuracyByCategoriesChart')

const userAccuracyByCategoriesChartData = {
    labels: userAccuracyByCategories.labels,
    datasets: [{
        label: 'Точность вашего планирования',
        barThickness: 13,
        maxBarThickness: 20,
        minBarLength: 2,
        data: userAccuracyByCategories.data,
        backgroundColor: userAccuracyByCategories.colors,

    }],
};


const userAccuracyByCategoriesConfig = {
  type: 'bar',
  data: userAccuracyByCategoriesChartData,
  options: {
        indexAxis: 'x',
        responsive: true,
        scales: {
            x: {
                grid: {
                    color: 'gray'
                }
            },
            y: {
                grid: {
                    color: 'gray' 
                }
            }
        }
    }
};


new Chart(userAccuracyByCategoriesCTX, userAccuracyByCategoriesConfig);

const userSuccessRateByCategoriesCTX = document.getElementById('userSuccessRateByCategoriesChart')

const userSuccessRateByCategoriesChartData = {
    labels: userSuccessRateByCategories.labels,
    datasets: [{
        label: 'Успешно выполненные задачи',
        barThickness: 13,
        maxBarThickness: 20,
        minBarLength: 2,
        data: userSuccessRateByCategories.data,
        backgroundColor: userSuccessRateByCategories.colors,

    }],
};

const userSuccessRateByCategoriesConfig = {
  type: 'bar',
  data: userSuccessRateByCategoriesChartData,
  options: {
        indexAxis: 'x',
        responsive: true,
        scales: {
            x: {
                grid: {
                    color: 'gray'
                }
            },
            y: {
                grid: {
                    color: 'gray' 
                }
            }
        }
    }
};

new Chart(userSuccessRateByCategoriesCTX, userSuccessRateByCategoriesConfig);

const countUserTasksByWeekdaysCTX = document.getElementById('countUserTasksByWeekdaysChart');


const countUserTasksByWeekdaysChartData = {
  labels: countUserTasksByWeekdays.labels,
  datasets: [{
    label: 'Задачи по дням недели',
    data: countUserTasksByWeekdays.data,
    backgroundColor: 'rgba(56, 248, 255, 0.4)',
    hoverOffset: 4,
    barThickness: 13,
    maxBarThickness: 20,
    minBarLength: 2,
  }],

};

const countUserTasksByWeekdaysConfig = {
    type: 'bar',
    data: countUserTasksByWeekdaysChartData,
    options: {
      indexAxis: 'x',
      responsive: true,
      scales: {
          x: {
              grid: {
                  color: 'gray'
              }
          },
          y: {
              grid: {
                  color: 'gray' 
              }
          }
      }
  }

}

new Chart(countUserTasksByWeekdaysCTX, countUserTasksByWeekdaysConfig)

const countUserSuccessfulPlannedTasksByCategoriesCTX = document.getElementById('countUserSuccessfulPlannedTasksByCategoriesChart');

const countUserSuccessfulPlannedTasksByCategoriesChartData = {
  labels: countUserSuccessfulPlannedTasksByCategories.labels,
  datasets: [{
    label: 'Задачи, в которых запланированное время совпадает с временем выполнения',
    data: countUserSuccessfulPlannedTasksByCategories.data,
    backgroundColor: countUserSuccessfulPlannedTasksByCategories.colors,
    hoverOffset: 4,
    barThickness: 13,
    maxBarThickness: 20,
    minBarLength: 2,

  }],

};

const countUserSuccessfulPlannedTasksByCategoriesConfig = {
    type: 'bar',
    data: countUserSuccessfulPlannedTasksByCategoriesChartData,
    options: {
      indexAxis: 'x',
      responsive: true,
      scales: {
          x: {
              grid: {
                  color: 'gray'
              }
          },
          y: {
              grid: {
                  color: 'gray' 
              }
          }
      }
  }

}

new Chart(countUserSuccessfulPlannedTasksByCategoriesCTX, countUserSuccessfulPlannedTasksByCategoriesConfig)

const commonUserAccuracyCTX = document.getElementById('commonUserAccuracyChart')

const commonUserAccuracyChartData = {
  datasets: [{
    label: 'Точность планирования',
    data: commonUserAccuracy.data,
    backgroundColor: commonUserAccuracy.colors,
    hoverOffset: 4
  }]
};

const commonUserAccuracyConfig = {
    type: 'doughnut',
    data: commonUserAccuracyChartData,
    options: { 
      elements: { 
        arc: { borderColor: "rgb(15, 15, 15)" } },
        plugins: {
            tooltip: {
                bodyFont: {
                    size: 9
                }
            }
        }
    }
}

new Chart(commonUserAccuracyCTX, commonUserAccuracyConfig)

const commonUserSuccessRateCTX = document.getElementById('commonUserSuccessRateChart')

const commonUserSuccessRateChartData = {
  datasets: [{
    label: 'Успешные задачи',
    data: commonUserSuccessRate.data,
    backgroundColor: commonUserSuccessRate.colors,
    hoverOffset: 4
  }]
};

const commonUserSuccessRateConfig = {
    type: 'doughnut',
    data: commonUserSuccessRateChartData,
    options: { 
      elements: { 
        arc: { borderColor: "rgb(15, 15, 15)" } },
        plugins: {
            tooltip: {
                bodyFont: {
                    size: 9
                }
            }
        }
    }
}

new Chart(commonUserSuccessRateCTX, commonUserSuccessRateConfig)


const commonCountUserSuccessfulPlannedTasksCTX = document.getElementById('commonCountUserSuccessfulPlannedTasksChart')

const commonCountUserSuccessfulPlannedTasksChartData = {
  datasets: [{
    label: 'Правильно спланированные задачи',
    data: commonCountUserSuccessfulPlannedTasks.data,
    backgroundColor: commonCountUserSuccessfulPlannedTasks.colors,
    hoverOffset: 4
  }]
};

const commonCountUserSuccessfulPlannedTasksConfig = {
    type: 'doughnut',
    data: commonCountUserSuccessfulPlannedTasksChartData,
    options: { 
      elements: { 
        arc: { borderColor: "rgb(15, 15, 15)" } },
        plugins: {
            tooltip: {
                bodyFont: {
                    size: 9
                }
            }
        }
    }
}

new Chart(commonCountUserSuccessfulPlannedTasksCTX, commonCountUserSuccessfulPlannedTasksConfig)
