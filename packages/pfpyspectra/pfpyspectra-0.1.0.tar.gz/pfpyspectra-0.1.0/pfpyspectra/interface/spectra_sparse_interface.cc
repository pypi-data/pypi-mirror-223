#include <stdio.h>

// FIXME: INFO宏
// #define DEBUG
#ifdef DEBUG
#define INFO(...)                                                              \
  do {                                                                         \
    fprintf(stdout, "[INFO  ]%s %s(Line %d): \n", __FILE__, __FUNCTION__,      \
            __LINE__);                                                         \
  } while (0)
#else
#define INFO(...)
#endif // DEBUG

#include <Eigen/Core>
#include <Eigen/Sparse>
#include <utility>

#include <Spectra/MatOp/SparseGenComplexShiftSolve.h>
#include <Spectra/MatOp/SparseGenMatProd.h>
#include <Spectra/MatOp/SparseGenRealShiftSolve.h>
#include <Spectra/MatOp/SparseSymMatProd.h>
#include <Spectra/MatOp/SparseSymShiftSolve.h>
#include <Spectra/MatOp/SymShiftInvert.h>

#include <Spectra/GenEigsComplexShiftSolver.h>
#include <Spectra/GenEigsRealShiftSolver.h>
#include <Spectra/GenEigsSolver.h>
#include <Spectra/SymEigsShiftSolver.h>
#include <Spectra/SymEigsSolver.h>
// #include <Spectra/SymGEigsSolver.h>
#include <Spectra/SymGEigsShiftSolver.h>
// #include <Spectra/DavidsonSymEigsSolver.h>

#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

using ComplexMatrix = Eigen::MatrixXcd;
using ComplexVector = Eigen::VectorXcd;
using SpMatrix = Eigen::SparseMatrix<double>;
using SpVector = Eigen::SparseVector<double>;

using Matrix = Eigen::MatrixXd;
using Vector = Eigen::VectorXd;

using Eigen::Index;

#include <Eigen/Core>
#include <utility>

Spectra::SortRule string_to_sortrule(const std::string &name) {
  std::unordered_map<std::string, Spectra::SortRule> rules = {
      {"LargestMagn", Spectra::SortRule::LargestMagn},
      {"LargestReal", Spectra::SortRule::LargestReal},
      {"LargestImag", Spectra::SortRule::LargestImag},
      {"LargestAlge", Spectra::SortRule::LargestAlge},
      {"SmallestMagn", Spectra::SortRule::SmallestMagn},
      {"SmallestReal", Spectra::SortRule::SmallestReal},
      {"SmallestImag", Spectra::SortRule::SmallestImag},
      {"SmallestAlge", Spectra::SortRule::SmallestAlge},
      {"BothEnds", Spectra::SortRule::BothEnds}};
  auto it = rules.find(name);
  if (it != rules.cend()) {
    return it->second;
  } else {
    std::ostringstream oss;
    oss << "There is no selection rule named: " << name << "\n"
        << "Available selection rules:\n";
    for (const auto &pair : rules) {
      oss << pair.first << "\n";
    }
    throw std::runtime_error(oss.str());
  }
}

/// \brief Run the computation and throw and error if it fails
template <typename ResultVector, typename ResultMatrix, typename Solver>
std::pair<ResultVector, ResultMatrix>
compute_and_check(Solver &eigs, const std::string &selection) {
  // Initialize and compute
  eigs.init();
  // Compute using the user provided selection rule
  eigs.compute(string_to_sortrule(selection));

  // Retrieve results
  if (eigs.info() == Spectra::CompInfo::Successful) {
    return std::make_pair(eigs.eigenvalues(), eigs.eigenvectors());
  } else {
    throw std::runtime_error(
        "The Spectra SymEigsSolver calculation has failed!");
  }
}

// TAG: 1 普通矩阵

/// \brief Call the Spectra::GenEigsSolver eigensolver
std::pair<ComplexVector, ComplexMatrix>
sparsegeneigssolver(const SpMatrix &mat, Index nvalues, Index nvectors,
                    const std::string &selection) {
  INFO();
  using SparseOp = Spectra::SparseGenMatProd<double>;

  // Construct matrix operation object using the wrapper class SparseSymMatProd
  SparseOp op(mat);
  // Spectra::SparseGenMatProd<double> op(mat);
  Spectra::GenEigsSolver<SparseOp> eigs(op, nvalues, nvectors);

  return compute_and_check<ComplexVector, ComplexMatrix>(eigs, selection);
}

/// \brief Call the Spectra::GenEigsRealShiftSolver eigensolver
std::pair<ComplexVector, ComplexMatrix>
sparsegeneigsrealshiftsolver(const SpMatrix &mat, Index nvalues, Index nvectors,
                             double sigma, const std::string &selection) {
  INFO();
  using SparseOp = Spectra::SparseGenRealShiftSolve<double>;
  SparseOp op(mat);
  Spectra::GenEigsRealShiftSolver<SparseOp> eigs(op, nvalues, nvectors, sigma);
  return compute_and_check<ComplexVector, ComplexMatrix>(eigs, selection);
}

/// \brief Call the Spectra::GenEigsComplexShiftSolver eigensolver
std::pair<ComplexVector, ComplexMatrix>
sparsegeneigscomplexshiftsolver(const SpMatrix &mat, Index nvalues,
                                Index nvectors, double sigmar, double sigmai,
                                const std::string &selection) {
  INFO();
  using SparseOp = Spectra::SparseGenComplexShiftSolve<double>;
  SparseOp op(mat);
  Spectra::GenEigsComplexShiftSolver<SparseOp> eigs(op, nvalues, nvectors,
                                                    sigmar, sigmai);
  return compute_and_check<ComplexVector, ComplexMatrix>(eigs, selection);
}

// TAG: 2 对称矩阵

/// \brief Call the Spectra::SparseSymMatProd eigensolver
std::pair<Vector, Matrix> sparsesymeigssolver(const SpMatrix &mat,
                                              Index nvalues, Index nvectors,
                                              const std::string &selection) {
  INFO();
  using SparseSym = Spectra::SparseSymMatProd<double>;
  // Construct matrix operation object using the wrapper class
  SparseSym op(mat);
  Spectra::SymEigsSolver<SparseSym> eigs(op, nvalues, nvectors);

  return compute_and_check<Vector, Matrix>(eigs, selection);
}

/// \brief Call the Spectra::SymEigsShiftSolver eigensolver
std::pair<Vector, Matrix>
sparsesymeigsshiftsolver(const SpMatrix &mat, Index nvalues, Index nvectors,
                         double sigma, const std::string &selection) {
  INFO();
  using SparseSymShift = Spectra::SparseSymShiftSolve<double>;
  // Construct matrix operation object using the wrapper class
  SparseSymShift op(mat);
  Spectra::SymEigsShiftSolver<SparseSymShift> eigs(op, nvalues, nvectors,
                                                   sigma);

  return compute_and_check<Vector, Matrix>(eigs, selection);
}

/// \brief Call the Spectra::SymGEigsShiftSolver eigensolver
std::pair<Vector, Matrix> sparsesymgeneigsshiftsolver(const SpMatrix &mat_A,
                                                const SpMatrix &mat_B,
                                                Index nvalues, Index nvectors,
                                                double sigma,
                                                const std::string &selection) {
  INFO();
  using SymShiftInvert =
      Spectra::SymShiftInvert<double, Eigen::Sparse, Eigen::Sparse>;
  using SparseSym = Spectra::SparseSymMatProd<double>;

  // Construct matrix operation object using the wrapper class
  SymShiftInvert op_A(mat_A, mat_B);
  SparseSym op_B(mat_B);
  Spectra::SymGEigsShiftSolver<SymShiftInvert, SparseSym,
                               Spectra::GEigsMode::ShiftInvert>
      eigs(op_A, op_B, nvalues, nvectors, sigma);

  return compute_and_check<Vector, Matrix>(eigs, selection);
}

// NOTE: 稀疏矩阵只支持copy
PYBIND11_MODULE(spectra_sparse_interface, m) {
  m.doc() = "Interface to the C++ spectra library, see: "
            "https://github.com/yixuan/spectra";

  m.def("sparse_general_eigensolver", &sparsegeneigssolver);

  m.def("sparse_general_real_shift_eigensolver", &sparsegeneigsrealshiftsolver);

  m.def("sparse_general_complex_shift_eigensolver",
        &sparsegeneigscomplexshiftsolver);

  m.def("sparse_symmetric_eigensolver", &sparsesymeigssolver);

  m.def("sparse_symmetric_shift_eigensolver", &sparsesymeigsshiftsolver);

  m.def("sparse_symmetric_generalized_shift_eigensolver",
        &sparsesymgeneigsshiftsolver);
}
